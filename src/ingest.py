"""
Ingestion system - loads story bible files into vector database
"""

import os
import glob
from dotenv import load_dotenv

#load env variables
load_dotenv()

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


def parse_markdown_file(file_path):
    print(f"Parsing {file_path}")

    with open(file_path, 'r', encoding='utf-8') as file:
        content = file.read()

    sections = []
    lines = content.split('\n')
    current_section = {"header": "", "content": "", "level": 0, "file": file_path}

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
    if current_section["content"].strip():
        sections.append(current_section.copy())

    return sections

def main():
    print("Story Bible Ingestion System")
    print("Environment Loaded")

    # Test Nerina file parsing
    # sections = parse_markdown_file("bible_content/characters/Character_Bible_NERINA_v1.10_LOCKED.md")

    all_sections = parse_all_bible_files()

    print(f"\nTotal sections found: {len(all_sections)}")

    # Show breakdown by category
    from collections import Counter
    categories = Counter(section['category'] for section in all_sections)
    for category, count in categories.items():
        print(f"  {category}: {count} sections")

    api_key = os.getenv('OPENAI_API_KEY')
    if api_key:
        print("OpenAI API key configured")
    else:
        print('OpenAI API key not found in .env file')

if __name__ == "__main__":
    main()