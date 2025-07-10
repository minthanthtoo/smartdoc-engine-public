from setuptools import setup

setup(
    name='smartdoc-cli',
    version='0.1',
    py_modules=['smartdoc_cli'],
    install_requires=['typer', 'pytesseract', 'pillow'],
    entry_points={
        'console_scripts': ['smartdoc=cli.smartdoc_cli:app'],
    },
)
