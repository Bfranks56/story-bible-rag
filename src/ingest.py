"""
Ingestion system - loads story bible files into vector database
"""

import os
import glob
from openai import OpenAI
from dotenv import load_dotenv
import json
import time
import faiss
import numpy as np
import pickle

#load env variables
load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

def create_faiss_index(sections):
    """Create FAISS index from sections with embeddings"""
    print("Creating FAISS index...")

    # Extract embeddingss and convert to numpy array
    embeddings = []
    metadata = []

    for section in sections:
        if 'embedding' in section:
            embeddings.append(section['embedding'])
            metadata.append({
                'header': section['header'],
                'content': section['content'],
                'level': section['level'],
                'file': section.get('file', 'unknown')
            })

    # convert to numpy array
    embedding_array = np.array(embeddings, dtype=np.float32)

    # create FAISS index (cosine similarity)
    dimension = embedding_array.shape[1] 
    index = faiss.IndexFlatIP(dimension)

    # Normailze vectors for cosine similarity
    faiss.normalize_L2(embedding_array)

    # add vectors to index
    index.add(embedding_array)

    print(f"FAISS index created with {index.ntotal} vectors")
    return index, metadata

def save_index_and_metadata(index, metadata, base_path="data/"):
    """Save FAISS index and metadata to disk"""
    os.makedirs(base_path, exist_ok=True)

    faiss.write_index(index, f"{base_path}story_bible.index")

    with open(f"{base_path}metadata.pkl", 'wb') as f:
        pickle.dump(metadata, f)

    print(f"Saved index and metadata to {base_path}")

def get_embeddings(text, model="text-embedding-3-small"):
    """Get embeddings for a piece of text"""
    try:
        response = client.embeddings.create(
            input=text,
            model=model
        )
        return response.data[0].embedding
    except Exception as e:
        print(f"Error getting embeddings: {e}")
        return None

def get_embeddings_batch(texts, model="text-embedding-3-small"):
     """Get embeddings for multiple texts at once (more efficient)"""
     try:
         response = client.embeddings.create(
             input=texts,
             model=model
         )
         return [item.embedding for item in response.data]
     except Exception as e:
         print(f"Error getting batch embeddings: {e}")
         return None



def parse_all_bible_files():
    """Parse all markdown files in the bible_content directory"""
    all_sections = []

    # Find all .md files in subdirectories
    pattern = "bible_content/**/*.md"
    files = glob.glob(pattern, recursive=True)

    print(f"Found {len(files)} files to process")

    for file_path in files:
        # Extract category from folder structure
        category = os.path.dirname(file_path).split('/')[-1]

        sections = parse_markdown_file(file_path)

        # Add category metadata to each section
        for section in sections:
            section['category'] = category

        all_sections.extend(sections)
        print(f" {file_path}: {len(sections)} sections")

    return all_sections


def parse_markdown_file(file_path, get_embeds=False):
    # print(f"Parsing {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    sections = []
    lines = content.split('\n')
    current_section = {"header": "", "content": "", "level": 0}

    for line in lines:
        if line.startswith('#'):
            # Save previous section if it has content
            if current_section["content"].strip():
                sections.append(current_section.copy())

            # Start a new section
            level = len(line) - len(line.lstrip('#'))
            header = line.lstrip("# ").strip()
            current_section = {
                "header": header,
                "content": "",
                "level": level,
                "file": file_path
            }
        else:
            current_section["content"] += line + "\n"

    # Append last section if it has content
    if current_section["content"].strip() and current_section["header"].strip():
        sections.append(current_section.copy())

    if get_embeds and sections:
        print(f" Getting embeddings for {len(sections)} sections...")
        texts = [f"{s['header']}\n{s['content']}" for s in sections]
        embeddings =get_embeddings_batch(texts)

    if embeddings:
        for i, embedding in enumerate(embeddings):
            sections[i]['embedding'] = embedding

    time.sleep(0.5)

    return sections

# def main():
#     print("Story Bible Ingestion System")
#     print("Environment Loaded")

#     # Test Nerina file parsing
#     # sections = parse_markdown_file("bible_content/characters/Character_Bible_NERINA_v1.10_LOCKED.md")

#     all_sections = parse_all_bible_files()

#     print(f"\nTotal sections found: {len(all_sections)}")

#     # Show breakdown by category
#     from collections import Counter
#     categories = Counter(section['category'] for section in all_sections)
#     for category, count in categories.items():
#         print(f"  {category}: {count} sections")

#     api_key = os.getenv('OPENAI_API_KEY')
#     if api_key:
#         print("OpenAI API key configured")
#     else:
#         print('OpenAI API key not found in .env file')
def main():
    print("Story Bible Ingestion System")
    print("Environment Loaded")
    
    # Test with just Nerina file first
    nerina_file = "bible_content/characters/Character_Bible_NERINA_v1.10.1_LOCKED.md"
    print(f"Testing embeddings with: {nerina_file}")
    
    sections = parse_markdown_file(nerina_file, get_embeds=True)
    print(f"Processed {len(sections)} sections")

    # Create and save FAISS index
    index, metadata = create_faiss_index(sections)
    save_index_and_metadata(index, metadata)

    print("FAISS index created and saved successfully!")

if __name__ == "__main__":
    main()