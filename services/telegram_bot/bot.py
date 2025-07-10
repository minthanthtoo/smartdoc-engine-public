import os
import asyncio
import aiohttp
import mimetypes
from dotenv import load_dotenv
from threading import Thread
import uvicorn
import file_server  # ✅ assumes file_server.py is in the same folder

from aiogram import Bot, Dispatcher, Router, types, F
from aiogram.enums import ContentType
from aiogram.types import FSInputFile, InlineKeyboardMarkup, InlineKeyboardButton, CallbackQuery
from aiogram.filters import Command

# === 🔧 Load .env config
env_file = ".env.prod" if os.getenv("ENV") == "production" else ".env.local"
load_dotenv(env_file)

TG_BOT_TOKEN = os.getenv("TG_BOT_TOKEN")
API_MAP = {
    "convert": os.getenv("CONVERT_API_URL"),
    "ocr": os.getenv("OCR_API_URL"),
    "compress": os.getenv("COMPRESS_API_URL"),
}
FILE_HOST_URL = os.getenv("FILE_HOST_URL")

# === 🤖 Setup Bot & Dispatcher
bot = Bot(token=TG_BOT_TOKEN)
dp = Dispatcher()
router = Router()
dp.include_router(router)

# === 🧩 UI Helpers
def build_command_keyboard():
    return InlineKeyboardMarkup(inline_keyboard=[
        [InlineKeyboardButton(text="🌀 Convert", callback_data="action:convert")],
        [InlineKeyboardButton(text="🧠 OCR", callback_data="action:ocr")],
        [InlineKeyboardButton(text="📦 Compress", callback_data="action:compress")],
    ])

def build_format_keyboard(action):
    if action == "convert":
        return InlineKeyboardMarkup(inline_keyboard=[
            [InlineKeyboardButton(text="PDF ➡️ DOCX", callback_data="format:docx")],
            [InlineKeyboardButton(text="PDF ➡️ TXT", callback_data="format:txt")],
            [InlineKeyboardButton(text="PDF ➡️ PNG", callback_data="format:png")],
        ])
    return None

# === 🧠 Per-user state (in-memory)
user_state = {}  # user_id -> { action, files[] }

# === /start Command
# === /start Command
@router.message(Command("start"))
async def cmd_start(msg: types.Message):
    print(f"🟢 /start by user {msg.from_user.id} ({msg.from_user.username})")
    await msg.answer(
        "👋 Welcome to SmartDoc Bot!\n\nChoose what you'd like to do:",
        reply_markup=build_command_keyboard()
    )

# === Action Selection Handler
@router.callback_query(F.data.startswith("action:"))
async def handle_action(callback: CallbackQuery):
    action = callback.data.split(":")[1]
    user_id = callback.from_user.id
    user_state[user_id] = {"action": action, "files": []}
    print(f"🛠️ User {user_id} selected action: {action}")
    await callback.message.answer(f"📤 Now send one or more files to `{action}`.")
    await callback.answer()

# === File Upload Handler
@router.message(F.document)
async def handle_file_upload(msg: types.Message):
    user_id = msg.from_user.id
    state = user_state.get(user_id)

    if not state:
        print(f"⚠️ File upload from user {user_id} without selecting action")
        await msg.answer("⚠️ Please choose an action first using /start.")
        return

    doc = msg.document
    state["files"].append(doc)
    count = len(state["files"])
    print(f"📩 Received file {count} from user {user_id}: {doc.file_name} ({doc.file_size/1024/1024:.2f} MB)")

    await msg.answer(
        f"✅ File {count} received. Send more or tap to proceed:",
        reply_markup=InlineKeyboardMarkup(
            inline_keyboard=[[InlineKeyboardButton(text="🚀 Start Processing", callback_data="process:start")]]
        )
    )

# === File Processing Handlerfrom tempfile import NamedTemporaryFile
from tempfile import NamedTemporaryFile
@router.callback_query(F.data == "process:start")
async def handle_process(callback: CallbackQuery):
    user_id = callback.from_user.id
    state = user_state.get(user_id)
    action = state.get("action")
    files = state.get("files", [])
    api_url = API_MAP.get(action)

    print(f"\n📦 Start processing {len(files)} file(s) for user {user_id}, action: {action}, API: {api_url}")

    if not files or not api_url:
        print(f"⚠️ No files or invalid API for user {user_id}")
        await callback.message.answer("⚠️ No files to process.")
        return

    await callback.answer()
    await callback.message.answer(f"📦 Starting `{action}` batch processing for {len(files)} file(s)...")

    for idx, doc in enumerate(files, 1):
        print(f"\n━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━")
        print(f"🔄 File {idx}/{len(files)}: {doc.file_name} ({doc.file_size/1024/1024:.2f} MB)")
        status = await callback.message.answer(f"⏳ Processing file {idx} of {len(files)}: `{doc.file_name}`")

        try:
            # Download file directly to disk
            print(f"⬇️ Starting to download via aiogram bot.download: {doc.file_id}")
            temp_file = NamedTemporaryFile(delete=False)
            await bot.download(doc, destination=temp_file)
            temp_file.close()
            print(f"📥 Downloaded to {temp_file.name} ({os.path.getsize(temp_file.name)/1024/1024:.2f} MB)")

            with open(temp_file.name, "rb") as f:
                content = f.read()

            async with aiohttp.ClientSession() as session:
                form = aiohttp.FormData()
                form.add_field("file", content, filename=doc.file_name, content_type="application/octet-stream")

                print(f"📤 Sending to {api_url}")
                async with session.post(api_url, data=form) as res:
                    if res.status != 200:
                        err_text = await res.text()
                        print(f"❌ API error {res.status}: {err_text}")
                        await status.edit_text(f"❌ API error: {err_text}")
                        continue

                    result = await res.read()
                    print(f"✅ API responded with {len(result)/1024/1024:.2f} MB")

                    mime = res.headers.get("Content-Type", "application/octet-stream")
                    ext = mimetypes.guess_extension(mime) or ".bin"
                    base, _ = os.path.splitext(doc.file_name)
                    filename = f"{base}_{action}{ext}"
                    path = f"/tmp/{filename}"

                    with open(path, "wb") as f:
                        f.write(result)
                    print(f"💾 Saved result to {path}")

                    file_size_mb = os.path.getsize(path) / 1024 / 1024
                    if file_size_mb <= 49.5:
                        print(f"📤 Sending back to Telegram: {filename} ({file_size_mb:.2f} MB)")
                        await bot.send_document(chat_id=user_id, document=FSInputFile(path, filename=filename))
                        await status.edit_text(f"✅ Done: `{filename}`")
                        print(f"📨 Sent back to user {user_id}")
                    else:
                        print(f"📛 File too large ({file_size_mb:.2f} MB), using file host fallback")
                        if FILE_HOST_URL:
                            try:
                                async with session.get(FILE_HOST_URL, timeout=3) as ping:
                                    if ping.ok:
                                        url = f"{FILE_HOST_URL.rstrip('/')}/{filename}"
                                        await status.edit_text(f"📎 File too large. Download here:\n🔗 {url}")
                                        print(f"🔗 File sent via link: {url}")
                                    else:
                                        raise Exception("File server not responding")
                            except Exception as e:
                                await status.edit_text("❌ File too large and file server is unreachable.")
                                print(f"❌ File host error: {e}")
                        else:
                            await status.edit_text("❌ File too large and FILE_HOST_URL is not configured.")
                            print("⚠️ FILE_HOST_URL is missing")

            os.unlink(temp_file.name)

        except Exception as e:
            await status.edit_text(f"❌ Unexpected error: {str(e)}")
            print(f"🚨 Exception during file processing: {e}")

    user_state[user_id]["files"] = []
    print(f"\n✅ All files processed for user {user_id}")
    print(f"━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━━\n")

# === 🔁 Start File Server in Thread
def start_file_server():
    uvicorn.run(file_server.app, host="0.0.0.0", port=8080, log_level="warning")

# === 🏁 Main Entrypoint
async def main():
    print("🚀 Starting threaded file server...")
    Thread(target=start_file_server, daemon=True).start()

    print("🤖 Starting SmartDoc Telegram Bot...")
    await dp.start_polling(bot)

if __name__ == "__main__":
    asyncio.run(main())