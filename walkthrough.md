# TriageBot Phase 1 Walkthrough

## Overview
We have successfully implemented the MVP for TriageBot. The system is designed to receive GitHub webhooks, classify issues using Gemini, route them to the appropriate team, apply labels, and generate a response.

## Components Implemented

### 1. Agents
- **ClassifierAgent** (`app/agents/classifier.py`): Uses Gemini 1.5 Flash to classify issues.
- **RouterAgent** (`app/agents/router.py`): Routes issues rule-based and keyword-based.
- **ResponderAgent** (`app/agents/responder.py`): Generates auto-replies with context.
- **SimilarityAgent** (`app/agents/similarity.py`): Detects duplicates using embeddings.
- **Orchestrator** (`app/agents/orchestrator.py`): Coordinates the flow between agents.

### 2. Services
- **GitHubService** (`app/services/github.py`): Handles labeling and commenting.
- **LLMService** (`app/services/llm.py`): Wrapper for Gemini API.
- **EmbeddingService** (`app/services/embedding.py`): Local embeddings using `sentence-transformers`.
- **VectorStoreService** (`app/services/vectorstore.py`): Vector storage using `chromadb`.


### 3. API & Security
- **Webhook Endpoint** (`app/api/v1/endpoints/webhooks.py`): Receives `issues` events.
- **Security** (`app/core/security.py`): Verifies GitHub webhook signatures.

## Verification
### Running Tests
Unit tests covering the agents are located in `tests/unit/`.
```bash
pytest tests/unit/
```

### Manual Testing
1. **Configure Environment**: Copy `.env.example` to `.env` and fill in `GEMINI_API_KEY`, `GITHUB_TOKEN`, and `GITHUB_WEBHOOK_SECRET`.
2. **Start Server**:
   ```bash
   uvicorn app.main:app --reload
   ```
3. **Trigger Webhook**: Use a tool like `ngrok` to expose your local server to GitHub, or use the `test_workflow.py` integration test (requires valid keys).

## Next Steps
- Deploy to Railway/Render using the provided `Dockerfile`.
- Set up the real GitHub webhook in your repository settings.
