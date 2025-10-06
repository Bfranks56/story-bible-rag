"""
Chat interface - combines search results with OpenAI chat completion
"""

import os
import datetime
from dotenv import load_dotenv
from openai import OpenAI
import faiss
import pickle
import numpy as np
from web_search import search_web

load_dotenv()
client = OpenAI(api_key=os.getenv('OPENAI_API_KEY'))

# Constants
SYSTEM_PROMPT = """You are a creative collaborator for the Black Horizon story bible.

VOICE & STYLE:
- Conversational and knowledgeable, like talking with a creative partner
- Casual but not over-the-top - natural language, not forced slang
- Occasional Star Wars, Hip Hop or mech anime references when they fit naturally
- Enthusiastic about the story without being gimmicky

SOURCE CITATION:
- Always cite sources at the start: [filename | section]
- Example: [Character_Bible_NERINA | Pilot Style]: Nerina's empathic grace...
- Make citations feel integrated, not jarring

CANON INTEGRITY:
- Ground everything in retrieved story bible content
- If context is missing: "I don't have that in the bible yet - want to explore it?"
- Don't improvise lore without explicit request
- Mark new suggestions clearly as ideas to develop

COLLABORATION:
- Frame as collaborative: "let's explore", "we could develop"
- Ask clarifying questions when helpful
- Suggest connections between story elements
- Help develop ideas while respecting canon"""


WEB_SEARCH_TRIGGERS = [
    " vs ", " versus ", " compared to ",
    "wing zero", "evangelion", "gundam",
    "what anime", "what mech anime", "similar to",
    "research", "inspiration from", "examples of"
]

CONTENT_GENERATION_TRIGGERS = [
    "expand", "add", "develop", "create", "suggest", 
    "what's missing", "fill in", "elaborate"
]

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

def _has_triggers(query, triggers):
    """Helper function to check if query contains any triggers"""
    query_lower = query.lower()
    return any(trigger in query_lower for trigger in triggers)

def should_search_web(query):
    """Determine if query would benefit from web search"""
    return _has_triggers(query, WEB_SEARCH_TRIGGERS)

def _build_context_sections(results, source_type, key_map):
    """Helper to build context sections from results"""
    sections = []
    for result in results:
        header_key, content_key = key_map
        if result.get(header_key, '').strip():
            section = f"[{source_type} | {result[header_key]}]\n{result[content_key]}\n"
            sections.append(section)
    return "\n---\n".join(sections)

def build_context_prompt(question, search_results, web_results=None):
    """Build a prompt with relevant context from both story bible and web"""
    
    # Story bible context
    story_context = _build_context_sections(
        search_results, "STORY BIBLE", ("header", "content")
    )
    
    # Web search context (if available)
    web_context = ""
    if web_results:
        web_context = _build_context_sections(
            web_results, "WEB", ("title", "snippet")
        )

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
    return _has_triggers(query, CONTENT_GENERATION_TRIGGERS)

def build_expansion_prompt(question, search_results):
     """Build prompt for generating new story bible content"""
     
     existing_context = _build_context_sections(
         search_results, "EXISTING", ("header", "content")
     )

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


def _call_openai_chat(prompt, system_prompt=SYSTEM_PROMPT, max_tokens=500, temperature=0.7):
    """Helper function to make OpenAI chat completion calls"""
    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role": "system", "content": system_prompt}, 
            {"role": "user", "content": prompt}
        ],
        temperature=temperature,
        max_tokens=max_tokens
    )
    return response.choices[0].message.content

def save_draft_content(content, character_name="GENERAL"):
    """Save AI-generated content to a DRAFT file"""
    timestamp = datetime.datetime.now().strftime("%Y%m%d_%H%M%S")
    filename = f"bible_content/drafts/{character_name}_DRAFT_{timestamp}.md"

    # Create drafts directory if it doesn't exist
    os.makedirs("bible_content/drafts", exist_ok=True)

    # Save content
    with open(filename, 'w') as f:
        f.write(content)

    return filename

def chat_with_bible(question):
    """Enhanced chat with story bible + web search"""
    print(f"Question: {question}")
    print("Searching for relevant content...")
    
    # Search for relevant sections
    search_results = search_story_bible(question, k=3)

    # Define meta-conversation triggers (questions ABOUT the story/themes)
    meta_triggers = ["like", "similar", "compared", "influence", "inspired by", 
                 "theme", "feel like", "reminds", "style"]

    is_meta_question = any(trigger in question.lower() for trigger in meta_triggers)


    # Check if query is story-related
    if not search_results or (all(r['similarity_score'] < 0.3 for r in search_results) and not is_meta_question):
        return "Yo, that's not related to Black Horizon. Let's keep it focused on the story bible - characters, mechs, plot, worldbuilding. What do you want to explore?"

    
    # Check if user wants to generate new content
    if should_generate_content(question):
        print("Generating new story bible content...")
        expansion_prompt = build_expansion_prompt(question, search_results)
        
        # Generate content with higher token limit for expansion
        generated_content = _call_openai_chat(expansion_prompt, max_tokens=800)

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
    
    # Get AI response using helper function
    return _call_openai_chat(prompt)

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