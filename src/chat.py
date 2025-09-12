"""
Chat interface - combines search results with OpenAI chat completion
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import faiss
import pickle
import numpy as np

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
    index, metadata = load_index_and_metadata()

    # get query embedding
    response = client.embeddings.create(
        input=query,
        model="text-embedding-3-small"
    )
    query_embedding = np.array([response.data[0].embedding], dtype=np.float32)

    # normalize for cosine similarity
    faiss.normalize_L2(query_embedding)

    # search
    scores, indices = index.search(query_embedding, k)

    # Return results
    results = []
    for score, idx in zip(scores[0], indices[0]):
        if idx != -1:
            result = metadata[idx].copy()
            result['similarity_score'] = float(score)
            results.append(result)

    return results

def build_context_prompt(question, search_results):
    """Build a prompt with relevant context"""
    context_sections = []

    for result in search_results:
        if result['header'].strip():
            section = f"Section: {result['header']}\n{result['content']}\n"
            context_sections.append(section)

    context = "\n---\n".join(context_sections)

    prompt = f"""Based on the following sections from a story bible, please answer the user's question.

CONTEXT FROM STORY BIBLE:
{context}

USER QUESTION: {question}

Please provide a helpful answer based on the provided context. If the context doesn't contain enough information to fully answer the question, say so and provide what information is available."""

    return prompt

def chat_with_bible(question):
    """Chat about story bible content using RAG"""
    print(f"Question: {question}")
    print("Searching for relevant content...")
    
    # Search for relevant sections
    search_results = search_story_bible(question, k=3)
    
    if not search_results:
        return "I couldn't find relevant information in the story bible for that question."
    
    # Build prompt with context
    prompt = build_context_prompt(question, search_results)
    
    print("Generating response...")
    
    # Get AI response
    response = client.chat.completions.create(
        model="gpt-3.5-turbo",
        messages=[{"role": "user", "content": prompt}],
        temperature=0.7,
        max_tokens=500
    )
    
    return response.choices[0].message.content

def main():
    print("Story Bible Chat Interface")
    print("Ask questions about your story bible content!")
    print("Type 'quit' to exit\n")
    
    while True:
        question = input("\nYour question: ").strip()
        
        if question.lower() in ['quit', 'exit', 'q']:
            print("Goodbye!")
            break
        
        if not question:
            continue
            
        try:
            answer = chat_with_bible(question)
            print(f"\nAnswer: {answer}")
        except Exception as e:
            print(f"Error: {e}")

if __name__ == "__main__":
    main()