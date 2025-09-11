"""
Search system - finds relevant content from vector database
"""

import os
from dotenv import load_dotenv

load_dotenv()

def search_content(query):
    """Search for relavant story bible content"""
    print(f"Searching for: '{query}'")
    #TODO: add vector serach logic
    return []

def main(): 
    print("story Bible Search System")
    print("Ready to search story content")

    #Test search
    results = search_content("Nerina core values")
    print(f"Found {len(results)} results")

if __name__ == "__main__":
    main()