#!/usr/bin/env bash
# Bootstraps SkillForge for local development.
# Usage: ./scripts/setup.sh
set -euo pipefail

ROOT_DIR="$(cd "$(dirname "${BASH_SOURCE[0]}")/.." && pwd)"
cd "$ROOT_DIR"

if [ ! -f .env ]; then
  echo "No .env found — copying .env.example. Edit it and add your ANTHROPIC_API_KEY before continuing."
  cp .env.example .env
  echo "Edit .env now, then re-run this script."
  exit 1
fi

echo "==> Building and starting all services (this can take a few minutes the first time)..."
docker compose up -d --build

echo "==> Waiting for Postgres to accept connections..."
until docker compose exec -T postgres pg_isready -U skillforge > /dev/null 2>&1; do
  sleep 2
done

echo "==> Seeding assessment question bank..."
docker compose --profile tools run --rm seed python scripts/seed_questions.py

echo "==> Seeding RAG knowledge base (downloads a small embedding model on first run)..."
docker compose --profile tools run --rm seed python -m services.ai.seed_kb

echo ""
echo "SkillForge is running:"
echo "  Frontend:        http://localhost:3000"
echo "  API Gateway:     http://localhost:8080"
echo "  Auth service:    http://localhost:8001/docs"
echo "  Core service:    http://localhost:8002/docs"
echo "  Analyzer service http://localhost:8003/docs"
echo "  AI service:      http://localhost:8004/docs"
echo ""
echo "Stop everything with: docker compose down"
