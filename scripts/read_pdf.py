from pypdf import PdfReader

pdf_path = "data/alchi.pdf"

reader = PdfReader(pdf_path)

print(f"Total Pages: {len(reader.pages)}")
print("-" * 50)

for page_num, page in enumerate(reader.pages):
    text = page.extract_text()

    print(f"\nPAGE {page_num + 1}")
    print("-" * 20)

    if text:
        print(text[:1000])  # first 1000 chars
    else:
        print("No text found")