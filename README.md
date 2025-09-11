# Story Bible RAG System

A Retrieval-Augmented Generation (RAG) system for maintaining consistent access to TV show/story bible content across long conversations.

## Problem Solved
ChatGPT loses context in long conversations about story elements. This system provides persistent memory of your story bible content.

## Current Status
✅ Project structure setup  
✅ Dependencies configured  
✅ Basic templates created  
✅ **File ingestion system working** - Successfully parsing 10 story bible files (151 sections)
✅ **Content categorization** - Organized into characters (65 sections), world (65 sections), story (21 sections)
✅ **Environment configuration** - OpenAI API key configured
🔄 **Next: Implement vector embeddings and search functionality**
🔄 **Next: Connect chat interface to search results**

## Quick Start

Currently functional:

- `python src/ingest.py` - Parse story bible files (working - processes 151 sections from 10 files)
- `python src/search.py` - Search interface template (needs vector implementation)  
- `python src/chat.py` - Chat interface template (needs search integration)

## Architecture

- src/ingest.py - ✅ Loads story bible files into structured sections
- src/search.py - 🔄 Semantic search for relevant content (template ready)
- src/chat.py - 🔄 Chat interface with context injection (template ready)
- bible_content/ - ✅ Story bible markdown files (10 files organized by category)
- data/ - 🔄 Vector database storage (next step)

## Dependencies

- FAISS for vector search
- OpenAI for embeddings and chat
- Python-frontmatter for markdown parsing
