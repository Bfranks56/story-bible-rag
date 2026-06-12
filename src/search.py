"""
Search system - finds relevant content from vector database
"""

import os
from dotenv import load_dotenv

load_dotenv()

def search_content(query):
    """Search for relevant story bible content.
    
    NOTE: Real search logic lives in chat.py (search_story_bible).
    This stub will be replaced when search_story_bible is migrated here (Phase 4).
    """
    raise NotImplementedError("Use search_story_bible() in chat.py")

def main(): 
    print("story Bible Search System")
    print("Ready to search story content")

    #Test search
    results = search_content("Nerina core values")
    print(f"Found {len(results)} results")

if __name__ == "__main__":
    main()