# 🧠 SmartDoc Engine

Modular AI-powered document API platform — Compress, Convert, OCR, Redact, Extract, and Analyze documents via REST or CLI.

![GitHub stars](https://img.shields.io/github/stars/yourorg/smart-doc)
![Docker Pulls](https://img.shields.io/docker/pulls/yourorg/smartdoc)
![License](https://img.shields.io/github/license/yourorg/smart-doc)
![Built with Python](https://img.shields.io/badge/built%20with-python-blue)

---

## 📦 Features

- ✅ PDF/Image Compression (Ghostscript, pikepdf)
- ✅ OCR with Tesseract
- ✅ Convert PDF ↔ DOCX ↔ TXT
- ✅ Redact content with regex or AI
- ✅ Extract tables, forms, and metadata
- ✅ Analyze docs (classify, summarize)

---

## 🚀 Quick Start

```bash
git clone https://github.com/yourorg/smart-doc
cd smart-doc
docker build -t smartdoc .
docker run -p 8000:8000 smartdoc

Use Swagger UI: http://localhost:8000/docs

⸻

🔧 Modules

Endpoint	Description
/api/v1/compress	Compress PDF/image/docx
/api/v1/ocr	OCR scanned images/PDFs
/api/v1/convert	Convert formats
/api/v1/redact	Redact data (manual or smart)
/api/v1/extract	Extract forms, tables, metadata
/api/v1/analyze	Classify, summarize, label docs


⸻

💬 Community
	•	Discord
	•	Twitter
	•	Contributing Guide

⸻

🏁 License

MIT for community edition — commercial license available for on-prem/enterprise.

---

## ✅ 3. 📊 Landing Page Mockup (Markdown Style for Static Pages)

```md
# SmartDoc Engine ⚙️

**The modular AI platform to compress, convert, OCR, redact, and extract intelligence from any document.**

---

## 🔥 Live Stats

| Metric                 | Value        |
|------------------------|--------------|
| ⭐ GitHub Stars         | 3,148         |
| 🚀 API Requests/day     | 1.2M+         |
| 🧑‍💼 Enterprise Users   | 82 companies |
| 🔐 On-Prem Installs     | 19 orgs       |

---

## 🧱 Modules

- 📉 Smart Compression (PDF, DOCX, Images)
- 🔍 OCR + Layout Parsing
- 🔁 PDF ↔ DOCX ↔ TXT Conversion
- 🖋️ Redaction & Digital Signing
- 🧾 Table & Form Data Extraction
- 🧠 AI Classification + Summary

---

## 💼 Pricing

| Plan       | Free       | Pro ($49/mo) | Enterprise |
|------------|------------|--------------|------------|
| API Credits| 500/month  | 20K/month    | Custom     |
| File Size  | 10MB max   | 100MB max    | Unlimited  |
| Features   | Basic      | All modules  | +AI, On-Prem|

---

## ✨ Try It Now

- API Docs: [localhost:8000/docs](http://localhost:8000/docs)
- Demo UI: [localhost:8501](http://localhost:8501)

[GitHub Repo →](https://github.com/yourorg/smart-doc)


⸻

