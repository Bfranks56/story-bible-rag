# Black Horizon AI Story Collaborator

An intelligent story development assistant that combines Retrieval-Augmented Generation (RAG) with web research to support creative collaboration on the Black Horizon / Paint It Black series. Evolved from a simple RAG system into a full AI collaborator that maintains canon fidelity while providing research-augmented creative support.

## Problem Solved
Traditional chat models lose context in extended story development sessions, leading to:

- Personality layer overwrites
- Context window overflow  
- Canon contradictions and lore inconsistencies
- Inability to research genre conventions and inspirations

This AI collaborator provides persistent, searchable memory of version-locked story bible content (v1.10.1 [LOCKED]) while intelligently augmenting responses with relevant external research when needed.

## Current Status - AI STORY COLLABORATOR (60% Complete)

**Core Functionality**
- **Hybrid search system**: Story bible RAG + intelligent web research
- **Context-aware routing**: Automatically detects when queries need external research  
- **Multi-source responses**: Combines internal canon with genre research seamlessly
- **Professional voice**: Conversational, knowledgeable creative partner with natural language
- **Source attribution**: Bold citations with clear formatting `**[filename | section]:**` 
- **Content generation**: AI can create new story bible sections and save drafts
- **Character-aware drafts**: Auto-detects character focus and names draft files accordingly
- **Intelligent content detection**: Automatically recognizes expansion/suggestion requests
- **Relevance filtering**: Keeps conversations focused on Black Horizon story bible content
- **Meta-conversation support**: Handles thematic discussions and external comparisons
- **Draft management**: Auto-saves generated content to `bible_content/drafts/`

**Technical Implementation**
- **File ingestion**: 313 story bible sections indexed in FAISS vector database
- **Vector embeddings**: OpenAI text-embedding-3-small with cosine similarity search
- **Interactive collaboration**: Research-augmented story development assistant
- **Query cost**: ~$0.0012 per query with current single-stage retrieval

**Critical Limitations**
- **No cross-session memory**: Conversations reset when program closes
- **Limited retrieval**: Only top 3 chunks (k=3) with 0.3 similarity threshold  
- **Single-stage search**: Pure vector similarity without intelligent ranking
- **Synonym problems**: "created" vs "designed" don't match well
- **Nuance issues**: Misses thematic connections between related sections

## Development Roadmap

**Thread Persistence - Priority 1**
- Save conversations to JSON files in `data/threads/` directory
- Enable loading previous threads by timestamp/preview
- Build conversation history into context for each query
- Allows resuming story development across days/weeks
- Multiple ongoing threads: "Nerina arc", "Season 1 plotting", "Mech designs"

**Two-Stage Retrieval - Priority 2**  
- **Stage 1**: FAISS search for top 15 candidates (cast wide net)
- **Stage 2**: GPT-4o-mini ranks candidates and selects top 5-7 most relevant
- Solves synonym matching, improves thematic understanding, filters noise
- Combines fast vector search with smart semantic ranking
- **Cost impact**: ~$0.0025 per query (2x increase for intelligent filtering)

### Optional Future Features

**Rolling Summary**
- Auto-compress conversation history every 5 messages
- Prevents token overflow in long story development sessions
- Maintains recent detail plus summarized older content

**Entity Tracking**
- Track characters/concepts discussed per thread
- Enable cross-thread references and knowledge graph
- Build story development context across conversations

**Multi-Stage Pipeline**
- Upgrade from single-pass to Plan → Draft → Critique → Revise workflow
- Higher quality expansions at 3.5x cost increase
- Professional-grade content generation

**Mode System**
- Command shortcuts: `/outline`, `/tldr`, `/polish`, `/brainstorm`
- Different thinking modes and response styles

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
bible_content/
├── characters/    - Character bible files (v1.10.1 LOCKED)
├── world/         - World-building files (v1.10.1 LOCKED)  
├── story/         - Story/plot files (v1.10.1 LOCKED)
├── drafts/        - AI-generated content drafts with timestamps
└── archive/       - Previous versions and archived content
data/              - FAISS vector database (story_bible.index, test_embeddings.json)
```

**Note**: The `bible_content/` directory contains proprietary story bible files for the Black Horizon series and is not included in this repository to protect intellectual property. Users should populate this directory with their own markdown files for the system to ingest and process.

**Version Management**: Current files are v1.10.1 LOCKED. Previous versions are archived in `bible_content/archive/` with organized subdirectories for characters, story, and world content.

**Critical Limitations (Blocking 77% Completion)**
- **No cross-session memory**: Conversations reset when program closes
- **Limited retrieval**: Only top 3 chunks (k=3) with 0.3 similarity threshold  
- **Single-stage search**: Pure vector similarity without intelligent ranking
- **Synonym problems**: "created" vs "designed" don't match well
- **Nuance issues**: Misses thematic connections between related sections

- **Hybrid Search**: Story bible RAG + web research via DuckDuckGo
- **Intelligent Routing**: Context-aware query classification and content generation detection
**Technical Implementation:**

- **Development Environment**: Python 3.11
- **Vector Search**: FAISS CPU with cosine similarity (313 indexed sections)
- **Embeddings**: OpenAI text-embedding-3-small  
- **AI Model**: OpenAI GPT-4o-mini with optimized context injection
- **Hybrid Search**: Story bible RAG + web research via DuckDuckGo
- **Intelligent Routing**: Context-aware query classification and content generation detection
- **Content Generation**: AI-powered story bible expansion with character-aware draft management
- **Relevance Filtering**: Similarity score thresholds with meta-conversation detection
- **Voice & Style**: Refined system prompts for natural, professional collaboration
- **Source Attribution**: Professional citation formatting with bold headers
- **Code Architecture**: DRY principles with helper functions and constants (270+ lines in `src/chat.py`)
- **Parsing**: Header-based chunking of markdown files
- **Draft System**: Character-aware timestamped auto-saving of generated content
- **Cost Efficiency**: ~$0.0012 per query (current), ~$0.0025 with two-stage retrieval

## Dependencies

- **Core AI**: OpenAI API (v1.51.0) for embeddings and chat completion  
- **Vector Search**: FAISS CPU (v1.12.0) for semantic similarity search
- **Web Research**: DuckDuckGo Search (v3.9.6+) for external context
- **File Processing**: python-frontmatter (v1.0.0) for markdown parsing
- **Environment**: python-dotenv (v1.0.0) for configuration management
- **HTTP**: httpx (v0.27.0) for async web requests
- **Data**: numpy (v1.26.0+), pandas (v2.1.0+) for data handling
- **Optional**: Streamlit (v1.28.0+) for future web interface

## Installation & Usage

**Setup:**

```bash
# Clone and navigate to project
git clone <repository-url>
cd story-bible-rag

# Create virtual environment  
python3 -m venv venv
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
# 1. Populate bible_content/ directory with your markdown files
# Structure: bible_content/{characters,world,story}/*.md

# 2. Ingest story bible files (creates vector database)
python src/ingest.py

# 3. Interactive AI story collaboration
python src/chat.py
```

**Enhanced Query Examples (What Works Right Now):**

**Story Bible Queries:**
- "What is Nerina's pilot style?" → retrieves relevant sections with citations
- "How does Tomas corrode Nerina's empathy?" → retrieves Phantom Drag/static corrosion mechanics
- "What is Fred's mask motif origin?" → cites Fred bible + Flashback bible anchor points  
- "Who created the Choir system?" → searches with design/development synonyms

**Hybrid Search (Story Bible + Web Research):**
- "Compare Nerina to Wing Zero" → searches story bible + web, combines sources
- "Evangelion compared to Black Horizon themes" → story context + external anime analysis
- "Mech anime inspiration for Choir refactor" → internal lore + genre conventions
- "What anime influenced Black Horizon?" → thematic analysis with external research

**Content Generation (AI Expansions):**
- "Expand Nerina's childhood training" → generates new content, saves to `NERINA_DRAFT_timestamp.md`
- "Add details to Nerina's combat techniques" → generates content, saves as character-specific draft
- "Suggest missing elements in Fred's arc" → AI creates new story bible entries in character-specific draft
- "Develop the static corrosion mechanics" → expands technical worldbuilding, saves as `GENERAL_DRAFT_timestamp.md`
- "Create more supporting character details" → generates content for SUPPORTING character draft

**Meta-Conversation (Thematic Analysis):**
- "What themes does Black Horizon explore?" → thematic analysis using story bible content
- "How is this similar to Evangelion?" → combines internal lore with external comparisons
- "What influences can you see in the worldbuilding?" → identifies patterns and inspirations
- "What makes this feel like a mech anime?" → style and genre analysis

## Recent Development History

**Latest Updates (December 2024):**
- Enhanced query logic with synonym expansion for better search coverage
- Improved prompting system for more natural collaboration
- Character layer refinements and personality tuning
- Version updates to v1.10.1 across all story bible files

**Canon-Guarded Personality Layer**
- Conversational, knowledgeable creative partner tone (not forced hip-hop/Star Wars)
- Natural language without gimmicks while maintaining enthusiasm
- Enhanced citation system: `**[filename | section]:**` with bold formatting
- Canon integrity with clear source grounding

**Professional Voice & Style**
- Refined system prompts for natural collaboration
- Professional citation formatting with bold headers
- Context-aware response generation

**Smart Content Management**
- Character-aware draft naming (NERINA_DRAFT, TOMAS_DRAFT, etc.)
- Automatic character detection from queries and search results
- Relevance filtering to keep conversations on-topic
- Meta-conversation support for thematic discussions

**Code Architecture Improvements**
- DRY principles applied throughout codebase
- Helper functions for common operations
- Constants for trigger lists and system prompts
- Centralized OpenAI API call handling

**Enhanced Query Intelligence**
- Content generation triggers: "expand", "add", "develop", "create", "suggest"
- Web search triggers: "vs", "compared to", anime/mech references, "similar to"
- Meta-conversation triggers: "like", "theme", "influenced by", "reminds"
- Query expansion with synonyms: "created/designed", "made/developed", "built/developed"
- Context-aware response routing for optimal information delivery
- Character detection from query content and search results

## Development Approach

**Incremental Implementation Philosophy:**
- Build features incrementally in small pieces
- Explain each function before coding  
- User manually types code for comprehension
- Test after each addition - one function at a time, no full file dumps
- This systematic method mirrors successful Angular learning and Ford interview prep

**Current Priority**: Implementing Thread Persistence (Priority 1) followed by Two-Stage Retrieval (Priority 2) to reach 77% completion and full usability as a creative collaborator.

---

*This system evolved from a simple RAG into a full AI story collaborator that solves real creative workflow problems: maintaining story consistency while providing intelligent research support for genre-aware creative development.*
