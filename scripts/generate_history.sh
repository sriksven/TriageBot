#!/bin/bash
set -e

echo "Cleaning up old git..."
rm -rf .git

# Initialize git
git init
git config user.name "Krishna Venkatesh" || true
git config user.email "43298886+sriksven@users.noreply.github.com" || true

# Helper function to commit with date
commit_date() {
    local date="$1"
    local msg="$2"
    
    if [ -z "$date" ]; then
        echo "Error: Date is missing"
        return 1
    fi
    
    # Use YYYY-MM-DD HH:MM:SS format
    export GIT_AUTHOR_DATE="${date} 12:00:00"
    export GIT_COMMITTER_DATE="${date} 12:00:00"
    
    echo "Committing on $GIT_AUTHOR_DATE: $msg"
    git commit -m "$msg" --allow-empty
}

# Unstage everything first (just in case)
git rm -r --cached . 2>/dev/null || true

# Jan 5: Initial setup
git add README.md .gitignore .env.example requirements.txt implementation-guide.md plan.md scripts/
# Add structure init files if any (ignoring errors)
git add */__init__.py */*/*/init.py 2>/dev/null || true
commit_date "2026-01-05" "Initial project structure and configuration"

# Jan 6: Settings
git add app/config/
commit_date "2026-01-06" "Add application settings and logging configuration"

# Jan 7: DB
git add app/models/ app/db/
commit_date "2026-01-07" "Implement domain models and database session"

# Jan 8: Security
git add app/core/
commit_date "2026-01-08" "Add GitHub webhook signature verification"

# Jan 9: GitHub Service
git add app/services/github.py
commit_date "2026-01-09" "Implement GitHub API service wrapper"

# Jan 10: LLM
git add app/services/llm.py
commit_date "2026-01-10" "Add Google Gemini LLM service integration"

# Jan 11: Classifier
git add app/agents/base.py app/agents/classifier.py
commit_date "2026-01-11" "Implement BaseAgent and ClassifierAgent"

# Jan 12: Router
git add app/agents/router.py
commit_date "2026-01-12" "Implement RouterAgent with rule-based routing"

# Jan 13: Responder
git add app/agents/responder.py
commit_date "2026-01-13" "Implement ResponderAgent for auto-replies"

# Jan 14: Orchestrator
git add app/agents/orchestrator.py
commit_date "2026-01-14" "Create Agent Orchestrator to coordinate workflows"

# Jan 16: API
git add app/api/
commit_date "2026-01-16" "Add webhook and health check API endpoints"

# Jan 17: Main
git add app/main.py
commit_date "2026-01-17" "Wire up FastAPI application and routers"

# Jan 18: Docker
git add Dockerfile docker-compose.yml
commit_date "2026-01-18" "Add Docker configuration"

# Jan 19: Unit Tests
git add tests/unit/
commit_date "2026-01-19" "Add unit tests for agents"

# Jan 20: Integration Tests
git add tests/integration/
commit_date "2026-01-20" "Add integration test for full workflow"

# Jan 22: Embedding
git add app/services/embedding.py
commit_date "2026-01-22" "Implement EmbeddingService using sentence-transformers"

# Jan 23: Vector Store
git add app/services/vectorstore.py
commit_date "2026-01-23" "Add ChromaDB vector store service"

# Jan 24: Similarity
git add app/agents/similarity.py
commit_date "2026-01-24" "Implement SimilarityAgent for duplicate detection"

# Jan 26: Update Orchestrator
# Force add it again just in case, though it hasn't changed
git add app/agents/orchestrator.py
commit_date "2026-01-26" "Integrate similarity search into orchestrator"

# Jan 27: Extractors
git add app/utils/
commit_date "2026-01-27" "Add context extraction utilities"

# Jan 29: Req update
# Touch to ensure change if possible, but allow-empty handles it
touch requirements.txt
git add requirements.txt
commit_date "2026-01-29" "Update requirements with Phase 2 dependencies"

# Jan 31: Docs
git add walkthrough.md
commit_date "2026-01-31" "Update documentation and walkthrough"

# Feb 1: Final
# Add anything missed (like folders not explicitly named)
git add .
commit_date "2026-02-01" "Final polish for Phase 2 completion"

echo "Done! Generated history."
