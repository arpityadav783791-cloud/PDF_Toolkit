import PyInstaller.__main__

PyInstaller.__main__.run([
    "main.py",
    "--name=PDFToolkit",
    "--windowed",
    "--clean",
])
