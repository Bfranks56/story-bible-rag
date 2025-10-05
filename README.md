# Black Horizon AI Story Collaborator

An intelligent story development assistant that combines Retrieval-Augmented Generation (RAG) with web research to support creative collaboration on the Black Horizon / Paint It Black series. Evolved from a simple RAG system into a full AI collaborator that maintains canon fidelity while providing research-augmented creative support.

## Problem Solved
Traditional chat models lose context in extended story development sessions, leading to:

- Personality layer overwrites
- Context window overflow  
- Canon contradictions and lore inconsistencies
- Inability to research genre conventions and inspirations

This AI collaborator provides persistent, searchable memory of version-locked story bible content (v1.10 [LOCKED]) while intelligently augmenting responses with relevant external research when needed.

## Current Status - AI STORY COLLABORATOR

- **Hybrid search system**: Story bible RAG + intelligent web research
- **Context-aware routing**: Automatically detects when queries need external research  
- **Multi-source responses**: Combines internal canon with genre research seamlessly
- **Source attribution**: Clear citations `[STORY BIBLE | section]` vs `[WEB | title]`
- **Content generation**: AI can create new story bible sections and save drafts
- **Intelligent content detection**: Automatically recognizes expansion/suggestion requests
- **Draft management**: Auto-saves generated content to `bible_content/drafts/`
- **File ingestion**: 151 sections parsed from 10 story bible files  
- **Vector embeddings**: FAISS database with OpenAI text-embedding-3-small
- **Interactive collaboration**: Research-augmented story development assistant
- **Content organization**: Characters (65 sections), world (65 sections), story (21 sections)

## Architecture

**File Structure:**

```text
src/
├── ingest.py      - Parses markdown files, creates embeddings, builds FAISS index
├── chat.py        - AI collaborator: hybrid search + content generation + draft saving
├── web_search.py  - DuckDuckGo integration for external research
├── search.py      - Standalone search interface (template)  
├── test_search.py - Search functionality testing utilities
└── __init__.py    
bible_content/     - Version-locked story bible files (characters/, world/, story/)
├── drafts/        - AI-generated content drafts with timestamps
data/              - FAISS vector database (story_bible.index, metadata.pkl)
```

**Technical Stack:**

- **Hybrid Search**: Story bible RAG + web research via DuckDuckGo
- **Intelligent Routing**: Context-aware query classification and content generation detection
- **Content Generation**: AI-powered story bible expansion with draft management
- **Vector Search**: FAISS with cosine similarity
- **Embeddings**: OpenAI text-embedding-3-small  
- **AI Collaboration**: OpenAI GPT-3.5-turbo with enhanced context injection
- **Source Attribution**: Multi-source citation system
- **Parsing**: Header-based chunking of markdown files
- **Draft System**: Timestamped auto-saving of generated content

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

**Content Generation Queries:**

- "Expand Tomas's childhood trauma" → creates new story bible section and saves draft
- "Add details to Nerina's combat techniques" → generates content based on existing canon
- "Suggest missing elements in Fred's arc" → AI creates new story bible entries
- "Develop the static corrosion mechanics" → expands technical worldbuilding content

## Recent Enhancements

**AI Content Generation**
- Automatic detection of expansion/suggestion requests  
- Smart content generation with canon consistency
- Draft file management with timestamps (`GENERAL_DRAFT_YYYYMMDD_HHMMSS.md`)
- Ready-to-review markdown format output

**Enhanced Query Intelligence**
- Content generation triggers: "expand", "add", "develop", "create", "suggest"
- Web search triggers: "vs", "compared to", anime/mech references
- Context-aware response routing for optimal information delivery

## Future Enhancements

**Canon-Guarded Personality Layer**

- Friendly, collaborative voice with hip-hop/Star Wars energy
- Enhanced citation system: `[STORY BIBLE | section]` and `[WEB | source]`
- Clear marking of CANON vs [SUGGESTION] vs [RESEARCH] content

**Advanced Content Workflow**  

- Draft review and approval system
- Auto-reingestion of approved drafts
- Version management (v1.10 → v1.10.1 patches)
- Integration testing for new content consistency

**Enhanced Collaboration Interface**

- Multi-turn conversation memory with research context
- Streamlit web interface for easier creative sessions
- Export research summaries and canon updates
- Batch content generation and organization tools

---

*This system evolved from a simple RAG into a full AI story collaborator that solves real creative workflow problems: maintaining story consistency while providing intelligent research support for genre-aware creative development.*
