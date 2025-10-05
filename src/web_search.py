from duckduckgo_search import DDGS

def search_web(query, max_results=3):
    """Simple web search function"""
    try:
        ddg = DDGS()
        results = ddg.text(query, max_results=max_results)

        search_results = []
        for result in results:
            search_results.append({
                'title': result.get('title', ''),
                'snippet': result.get('body', ''),
                'url': result.get('href', '')
            })
        return search_results
    except Exception as e:
        print(f"Search error: {e}")
        return []
    
# Test it
if __name__ == "__main__":
    results = search_web("Wing Zero Gundam pilot system")
    for result in results:
        print(f"Title: {result['title']}")
        print(f"Snippet: {result['snippet'][:100]}...")
        print("---")