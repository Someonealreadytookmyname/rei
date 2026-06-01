from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter

pdf_path = "data/alchi.pdf"

reader = PdfReader(pdf_path)

full_text = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        full_text += text + "\n"

print(f"Total Characters: {len(full_text)}")

splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_text(full_text)

print(f"\nTotal Chunks Created: {len(chunks)}")

for i, chunk in enumerate(chunks[:3]):
    print(f"\n--- CHUNK {i+1} ---")
    print(chunk[:500])