# Black Horizon AI Story Collaborator

An intelligent story development assistant that combines Retrieval-Augmented Generation (RAG) with web research to support creative collaboration on the Black Horizon / Paint It Black series. Evolved from a simple RAG system into a full AI collaborator that maintains canon fidelity while providing research-augmented creative support.

## Problem Solved
Traditional chat models lose context in extended story development sessions, leading to:

- Personality layer overwrites
- Context window overflow  
- Canon contradictions and lore inconsistencies
- Inability to research genre conventions and inspirations

This AI collaborator provides persistent, searchable memory of version-locked story bible content (v1.10 [LOCKED]) while intelligently augmenting responses with relevant external research when needed.

## Current Status - AI STORY COLLABORATOR ✅

✅ **Hybrid search system**: Story bible RAG + intelligent web research
✅ **Context-aware routing**: Automatically detects when queries need external research  
✅ **Multi-source responses**: Combines internal canon with genre research seamlessly
✅ **Source attribution**: Clear citations `[STORY BIBLE | section]` vs `[WEB | title]`
✅ **File ingestion**: 151 sections parsed from 10 story bible files  
✅ **Vector embeddings**: FAISS database with OpenAI text-embedding-3-small
✅ **Interactive collaboration**: Research-augmented story development assistant
✅ **Content organization**: Characters (65 sections), world (65 sections), story (21 sections)

## Architecture

**File Structure:**

```text
src/
├── ingest.py      - ✅ Parses markdown files, creates embeddings, builds FAISS index
├── chat.py        - ✅ AI collaborator: hybrid search + context + intelligent responses
├── web_search.py  - ✅ DuckDuckGo integration for external research
├── search.py      - 🔄 Standalone search interface (template)  
└── __init__.py    
bible_content/     - ✅ Version-locked story bible files (characters/, world/, story/)
data/              - ✅ FAISS vector database (story_bible.index, metadata.pkl)
```

**Technical Stack:**

- **Hybrid Search**: Story bible RAG + web research via DuckDuckGo
- **Intelligent Routing**: Context-aware query classification
- **Vector Search**: FAISS with cosine similarity
- **Embeddings**: OpenAI text-embedding-3-small  
- **AI Collaboration**: OpenAI GPT-3.5-turbo with enhanced context injection
- **Source Attribution**: Multi-source citation system
- **Parsing**: Header-based chunking of markdown files

## Dependencies

- **Core AI**: OpenAI API for embeddings and chat completion
- **Vector Search**: FAISS for semantic similarity search
- **Web Research**: DuckDuckGo Search (`ddgs`) for external context
- **File Processing**: python-frontmatter for markdown parsing
- **Environment**: python-dotenv for configuration management

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

# 2. Interactive AI story collaboration
python src/chat.py
```

**Enhanced Query Examples:**

**Story Bible Queries:**

- "How does Tomas corrode Nerina's empathy?" → retrieves Phantom Drag/static corrosion mechanics
- "What is Fred's mask motif origin?" → cites Fred bible + Flashback bible anchor points  
- "Describe Nerina's pilot style" → pulls character bible combat sections

**Research-Augmented Queries:**

- "Wing Zero vs Nerina's pilot system" → combines story bible + Gundam Wing research
- "Evangelion compared to Black Horizon themes" → story context + external anime analysis
- "Mech anime inspiration for Choir refactor" → internal lore + genre conventions

## Future Enhancements

🔄 **Canon-Guarded Personality Layer**

- Friendly, collaborative voice with hip-hop/Star Wars energy
- Enhanced citation system: `[STORY BIBLE | section]` and `[WEB | source]`
- Clear marking of CANON vs [SUGGESTION] vs [RESEARCH] content

🔄 **Advanced Research Integration**  

- Smarter query classification for hybrid search
- Genre-specific research triggers (mech anime, sci-fi tropes)
- Cross-reference validation between internal canon and external sources

🔄 **Content Update Workflow**  

- Research-informed content proposals
- Propose → Review → Approve → Re-ingest cycle with external validation
- Version management (v1.10 → v1.10.1 patches)

🔄 **Enhanced Collaboration Interface**

- Multi-turn conversation memory with research context
- Streamlit web interface for easier creative sessions
- Export research summaries and canon updates

---

*This system evolved from a simple RAG into a full AI story collaborator that solves real creative workflow problems: maintaining story consistency while providing intelligent research support for genre-aware creative development.*
