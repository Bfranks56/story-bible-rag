# Story Bible RAG System

A Retrieval-Augmented Generation (RAG) system for maintaining consistent access to TV show/story bible content across long conversations.

## Problem Solved
ChatGPT loses context in long conversations about story elements. This system provides persistent memory of your story bible content.

## Current Status
✅ Project structure setup  
✅ Dependencies configured  
✅ Basic templates created  
🔄 Next: Implement vector search and file processing  

## Quick Start
python src/ingest.py
python src/search.py  
python src/chat.py

## Architecture
src/ingest.py - Loads story bible files into vector database
src/search.py - Semantic search for relevant content
src/chat.py - Chat interface with context injection
bible_content/ - Story bible markdown files
data/ - Vector database storage

## Dependencies

FAISS for vector search
OpenAI for embeddings and chat
Python-frontmatter for markdown parsing