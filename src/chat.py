"""
Chat interface - main user interaction system
"""
import os
from dotenv import load_dotenv

load_dotenv()

def chat_with_bible(question):
    """Chat about story bible content"""
    print(f"💬 Question: {question}")
    # TODO: Add search + AI response logic
    return "This will be connected to your story bible soon!"

def main():
    print("💬 Story Bible Chat System")
    print("✅ Ready to answer questions about your story")
    
    # Test question
    response = chat_with_bible("What is Nerina's pilot style?")
    print(f"Response: {response}")

if __name__ == "__main__":
    main()