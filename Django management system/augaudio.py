from pypdf import PdfReader
from gtts import gTTS

pdf_file = "Module 2.pdf"
mp3_file = "output.mp3"

reader = PdfReader(pdf_file)

pdf_text = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        pdf_text += text + "\n"

if pdf_text.strip():
    audio = gTTS(text=pdf_text, lang="en")
    audio.save(mp3_file)
    print("PDF converted to MP3 successfully:", mp3_file)
else:
    print("No readable text was found in the PDF.")