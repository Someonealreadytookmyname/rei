from pypdf import PdfReader
from langchain_text_splitters import RecursiveCharacterTextSplitter
from sentence_transformers import SentenceTransformer
import chromadb

# Load PDF
reader = PdfReader("data/alchi.pdf")

full_text = ""

for page in reader.pages:
    text = page.extract_text()
    if text:
        full_text += text + "\n"

# Chunk text
splitter = RecursiveCharacterTextSplitter(
    chunk_size=1000,
    chunk_overlap=200
)

chunks = splitter.split_text(full_text)

print(f"Chunks created: {len(chunks)}")

# Embedding model
model = SentenceTransformer("all-MiniLM-L6-v2")

# Create embeddings
embeddings = model.encode(chunks)

# ChromaDB persistent storage
client = chromadb.PersistentClient(path="./chroma_db")

collection = client.get_or_create_collection(
    name="study_notes"
)

# Store chunks
for i, (chunk, embedding) in enumerate(zip(chunks, embeddings)):
    collection.add(
        ids=[str(i)],
        documents=[chunk],
        embeddings=[embedding.tolist()]
    )

print("Data stored successfully!")
print(f"Total records: {collection.count()}")