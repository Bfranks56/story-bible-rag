"""
Chat interface - combines search results with OpenAI chat completion
"""

import os
from dotenv import load_dotenv
from openai import OpenAI
import faiss
import pickle
import numpy as np
from web_search import search_web

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

def should_search_web(query):
    """Determine if query would benefit from web search"""
    web_triggers = [
        " vs ", " versus ", " compared to ", 
        "gundam", "wing zero", "evangelion", "anime", "mech",
        "research", "inspiration", "examples"
    ]

    query_lower = query.lower()
    return any(trigger in query_lower for trigger in web_triggers)

def build_context_prompt(question, search_results, web_results=None):
    """Build a prompt with relevant context from both story bible and web"""
    
    # Story bible context
    context_sections = []
    for result in search_results:
        if result['header'].strip():
            section = f"[STORY BIBLE | {result['header']}]\n{result['content']}\n"
            context_sections.append(section)

    story_context = "\n---\n".join(context_sections)
    
    # Web search context (if available)
    web_context = ""
    if web_results:
        web_sections = []
        for result in web_results:
            section = f"[WEB | {result['title']}]\n{result['snippet']}\n"
            web_sections.append(section)
        web_context = "\n---\n".join(web_sections)

    # Build the prompt
    prompt_parts = []
    
    if story_context:
        prompt_parts.append(f"STORY BIBLE CONTEXT:\n{story_context}")
    
    if web_context:
        prompt_parts.append(f"EXTERNAL CONTEXT:\n{web_context}")
    
    prompt_parts.append(f"USER QUESTION: {question}")
    prompt_parts.append("Please provide a helpful answer with source citations like [STORY BIBLE | section] or [WEB | title].")

    return "\n\n".join(prompt_parts)


def should_generate_content(query):
    """Detect if user wants AI to generate new story bible content"""
    expansion_triggers = [
        "expand", "add", "develop", "create", "suggest", 
        "what's missing", "fill in", "elaborate"
    ]
    
    query_lower = query.lower()
    return any(trigger in query_lower for trigger in expansion_triggers)

def build_expansion_prompt(question, search_results):
     """Build prompt for generating new story bible content"""

     context_sections = []
     for result in search_results:
         if result['header'].strip():
            section = f"[EXISTING | {result['header']}]\n{result['content']}\n"
            context_sections.append(section)
            
     existing_context = "\n---\n".join(context_sections)

     prompt = f"""You are helping expand a story bible for the Black Horizon series.

     EXISTING STORY BIBLE CONTENT:
     {existing_context}

     USER REQUEST: {question}

     Generate a new story bible section in proper markdown format:
        - Use ## for section headers
        - Keep the tone consistent with existing content
        - Add specific, concrete details
        - Stay true to established canon

     Format your response as a ready-to-save markdown section."""

     return prompt


def save_draft_content(content, character_name="GENERAL"):
    """Save AI-generated content to a DRAFT file"""
    import datetime

    #create timestamp for unique filename
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")

    #create filename
    filename = f"bible_content/drafts/{character_name}_DRAFT_{timestamp}.md"

    # Create drafts directory if it doesn't exist
    os.makedirs("bible_content/drafts", exist_ok=True)

    #save content
    with open(filename, 'w') as f:
        f.write(content)

    return filename

def chat_with_bible(question):
    """Enhanced chat with story bible + web search"""
    print(f"Question: {question}")
    print("Searching for relevant content...")
    
    # Search for relevant sections
    search_results = search_story_bible(question, k=3)
    
    # Check if user wants to generate new content (MOVE THIS UP)
    if should_generate_content(question):
        print("Generating new story bible content...")
        expansion_prompt = build_expansion_prompt(question, search_results)

        # Generate content
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user","content": expansion_prompt}],
            temperature=0.7,
            max_tokens=800
        )

        generated_content = response.choices[0].message.content

        # Save to draft file
        draft_file = save_draft_content(generated_content)

        return f"Generated new content and saved to: {draft_file}\n\nPREVIEW:\n{generated_content}"
    
    # Check if we should also search the web
    web_results = None
    if should_search_web(question):
        print("Also searching web for external context...")
        web_results = search_web(question, max_results=3)
    
    if not search_results and not web_results:
        return "I couldn't find relevant information for that question."
    
    # Build prompt with context
    prompt = build_context_prompt(question, search_results, web_results)
    
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