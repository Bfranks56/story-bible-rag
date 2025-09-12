# Black Horizon Story Bible RAG System

A Retrieval-Augmented Generation (RAG) system for preserving story bible content and enabling consistent creative collaboration on the Black Horizon / Paint It Black series. Built to solve ChatGPT's context loss problem in long creative conversations while maintaining canon fidelity.

## Problem Solved
Traditional chat models lose context in extended story development sessions, leading to:

- Personality layer overwrites
- Context window overflow  
- Canon contradictions and lore inconsistencies

This RAG system provides persistent, searchable memory of version-locked story bible content (v1.10 [LOCKED]) while enabling creative brainstorming grounded in established canon.

## Current Status - FULLY FUNCTIONAL RAG PIPELINE ✅

✅ **Complete end-to-end RAG system working**
✅ **File ingestion**: 151 sections parsed from 10 story bible files  
✅ **Vector embeddings**: FAISS database with OpenAI text-embedding-3-small
✅ **Semantic search**: Retrieves relevant context with similarity scoring
✅ **Interactive chat**: Questions answered using retrieved story bible content
✅ **Content organization**: Characters (65 sections), world (65 sections), story (21 sections)
✅ **Environment configuration**: OpenAI API integration functional

## Architecture

**File Structure:**

```text
src/
├── ingest.py      - ✅ Parses markdown files, creates embeddings, builds FAISS index
├── search.py      - 🔄 Standalone search interface (template)  
├── chat.py        - ✅ Full RAG pipeline: search + context + AI response
└── __init__.py    
bible_content/     - ✅ Version-locked story bible files (characters/, world/, story/)
data/              - ✅ FAISS vector database (story_bible.index, metadata.pkl)
```

**Technical Stack:**

- **Vector Search**: FAISS with cosine similarity
- **Embeddings**: OpenAI text-embedding-3-small  
- **Chat**: OpenAI GPT-3.5-turbo with context injection
- **Parsing**: Header-based chunking of markdown files
- **Metadata**: File source, section headers, similarity scores

## Dependencies

- FAISS for vector search
- OpenAI for embeddings and chat
- Python-frontmatter for markdown parsing

## Installation & Usage

**Setup:**

```bash
# Clone and navigate to project
cd story-bible-rag

# Create virtual environment
python -m venv venv
source venv/bin/activate  # On macOS/Linux
# venv\Scripts\activate    # On Windows

# Install dependencies
pip install -r requirements.txt

# Configure OpenAI API key
cp .env.example .env
# Edit .env with your OPENAI_API_KEY
```

**Usage:**

```bash
# 1. Ingest story bible files (creates vector database)
python src/ingest.py

# 2. Interactive chat with story bible
python src/chat.py
```

**Sample Queries:**

- "How does Tomas corrode Nerina's empathy?" → retrieves Phantom Drag/static corrosion mechanics
- "What is Fred's mask motif origin?" → cites Fred bible + Flashback bible anchor points  
- "Describe Nerina's pilot style" → pulls character bible combat sections

## Future Enhancements

🔄 **Canon-Guarded Personality Layer**

- Friendly, collaborative voice with hip-hop/Star Wars energy
- [file | section] citation system for all responses
- Clear marking of CANON vs [SUGGESTION] content

🔄 **Content Update Workflow**  

- Propose → Review → Approve → Re-ingest cycle
- Version management (v1.10 → v1.10.1 patches)
- Canon guardrails: refuse to improvise when context missing

🔄 **Enhanced Interaction**

- Multi-turn conversation memory
- Expanded search with multiple retrieval strategies
- Streamlit web interface for easier collaboration

---

*This system solves a real creative workflow problem: maintaining story consistency across long development sessions while enabling creative exploration grounded in established canon.*
