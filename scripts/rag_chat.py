import chromadb
from sentence_transformers import SentenceTransformer
from ollama import chat

# Load embedding model
embedding_model = SentenceTransformer("all-MiniLM-L6-v2")

# Connect to ChromaDB
client = chromadb.PersistentClient(path="chroma_db")

collection = client.get_collection("study_notes")

while True:
    question = input("\nAsk a question (or 'exit'): ")

    if question.lower() == "exit":
        break

    # Convert question to embedding
    question_embedding = embedding_model.encode(question).tolist()

    # Retrieve top chunks
    results = collection.query(
        query_embeddings=[question_embedding],
        n_results=3
    )

    context = "\n\n".join(results["documents"][0])

    prompt = f"""
Answer the question using ONLY the provided context.

Context:
{context}

Question:
{question}

Answer:
"""

    response = chat(
        model="qwen3:4b",
        messages=[
            {
                "role": "user",
                "content": prompt
            }
        ]
    )

    print("\nAnswer:")
    print(response["message"]["content"])