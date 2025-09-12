import faiss
import pickle
import numpy as np
from openai import OpenAI
from dotenv import load_dotenv
import os

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def load_index_and_metadata(base_path="data/"):
    """Load FAISS index and metadata from disk"""
    index = faiss.read_index(f"{base_path}story_bible.index")

    with open(f"{base_path}metadata.pkl", 'rb') as f:
        metadata = pickle.load(f)

    return index, metadata

def search_story_bible(query, k=3):
    """Search the story bible for relevant sections"""
    print(f"Searching for: '{query}'")

    # Load index and metadata
    index, metadata = load_index_and_metadata()

    # get query embedding
    response = client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    query_embedding = np.array([response.data[0].embedding], dtype=np.float32)

    # Normalize for cosine similarity
    faiss.normalize_L2(query_embedding)

    # Search
    scores, indices = index.search(query_embedding, k)

    # Return results
    results = []
    for i, (score, idx) in enumerate(zip(scores[0], indices[0])):
        if idx != -1:
            result = metadata[idx].copy()
            result['similarity_score'] = float(score)
            results.append(result)

    return results

def main():
    print("Story Bible Search Test")
    
    # Test queries about Nerina
    test_queries = [
        "Nerina's pilot style",
        "How does Nerina feel about emotions",
        "Nerina's relationship with Tomas",
        "empathy and war"
    ]
    
    for query in test_queries:
        print(f"\n{'='*50}")
        results = search_story_bible(query, k=2)
        
        for i, result in enumerate(results):
            print(f"\nResult {i+1} (Score: {result['similarity_score']:.3f}):")
            print(f"Section: {result['header']}")
            print(f"Content preview: {result['content'][:150]}...")

if __name__ == "__main__":
    main()