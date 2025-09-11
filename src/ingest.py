"""
Ingestion system - loads story bible files into vector database
"""

import os
from dotenv import load_dotenv

#load env variables
load_dotenv()

def main():
    print("Story Bible Ingestion System")
    print("Environment Loaded")
    print("Ready to process markdown files")

    # TODO: Add file processing logic
    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("OpenAI API key configured")
    else:
        print('OpenAI API key not found in .env file')

if __name__ == "__main__":
    main()