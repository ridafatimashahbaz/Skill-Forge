# SkillForge

AI-powered platform that evaluates a student's current skills and generates a
practical career development roadmap. Built for PS-03, LoopLab Looplearn
Hackathon 2026.

- [`docs/architecture.md`](docs/architecture.md) — service breakdown, diagram, agent tools
- [`docs/db-schema.md`](docs/db-schema.md) — database schema

## What's included

- **Student flow**: signup → profile (education, skills, projects,
  certifications, career goal) → skill assessment (Python, Web Development,
  Git, DevOps, AI, Database) → skill-gap analysis → generated roadmap → AI
  assistant (RAG chat and an agentic career-planning assistant)
- **Mentor/Admin flow**: browse students, view their profiles
- **Auth & RBAC**: JWT-based, three roles (student/mentor/admin)
- **Microservices**: Auth, Core (profile), Analyzer (Python/OOP scoring
  engine), AI (RAG + agent), behind an Nginx API gateway
- **DevOps**: Docker Compose (local), Kubernetes manifests, Terraform
  (managed Postgres + container registry), a seed shell script, GitHub
  Actions CI

## Run it on your laptop

**Requirements**: Docker Desktop (or Docker Engine + Compose) installed and
running. That's the only requirement — everything else runs inside
containers.

```bash
git clone <your-repo-url>
cd skillforge

cp .env.example .env
# edit .env and set ANTHROPIC_API_KEY (get one at https://console.anthropic.com/)
# JWT_SECRET can be any random string

./scripts/setup.sh
```

This builds and starts every service, waits for Postgres, and seeds both the
assessment question bank and the RAG knowledge base. First run takes a few
minutes (Docker image builds + a one-time embedding-model download by the AI
service — it needs normal internet access for that).

When it's done:

| What | URL |
|---|---|
| App (frontend) | http://localhost:3000 |
| API Gateway | http://localhost:8080 |
| Auth service docs | http://localhost:8001/docs |
| Core service docs | http://localhost:8002/docs |
| Analyzer service docs | http://localhost:8003/docs |
| AI service docs | http://localhost:8004/docs |

Sign up as a **student** to try the main flow, or as a **mentor**/**admin** to
see the student-browsing dashboard.

Stop everything: `docker compose down`. Wipe all data too: `docker compose down -v`.

**If you don't have Docker**: install Docker Desktop from
https://www.docker.com/products/docker-desktop/ — there's no supported way to
run this without containers, since it's genuinely five separate services plus
two databases.

## Push it to GitHub

```bash
git init
git add .
git commit -m "SkillForge: PS-03 submission"

# create an empty repo on github.com first (no README/license, so it stays empty), then:
git remote add origin https://github.com/<your-username>/<your-repo-name>.git
git branch -M main
git push -u origin main
```

That's your GitHub repository link for submission:
`https://github.com/<your-username>/<your-repo-name>`

## Deploy it live (get a public link)

This uses [Render](https://render.com)'s free tier via the included
`render.yaml` blueprint — no payment info needed, ~10 minutes.

1. Push this repo to GitHub (steps above) if you haven't.
2. Go to https://dashboard.render.com/blueprints → **New Blueprint Instance**.
3. Connect your GitHub account and select this repository. Render reads
   `render.yaml` automatically and lists everything it's about to create:
   a Postgres database, five private backend services, and two public
   services (`gateway`, `frontend`).
4. When prompted, paste your **ANTHROPIC_API_KEY**. Everything else
   (`JWT_SECRET`, database credentials, internal service URLs) is filled in
   automatically.
5. Click **Apply**. Render builds and starts every service — first deploy
   takes 10-15 minutes since it's building 7 Docker images.
6. Once it's live, open the **frontend** service in the Render dashboard —
   its URL (`https://skillforge-frontend-xxxx.onrender.com`) is your public
   link. Share that.
7. One manual step Render can't automate: seed the data. In the Render
   dashboard, open the **analyzer** service → **Shell**, and run:
   ```bash
   python scripts/seed_questions.py
   ```
   Then open the **ai** service → **Shell** and run:
   ```bash
   python -m services.ai.seed_kb
   ```
   (Only needed once — the data persists after that.)

**Free-tier note**: Render's free private services spin down after inactivity
and take ~30-60 seconds to wake up on the next request — normal for a
hackathon demo link, not something to worry about.

## Deploying to Kubernetes instead

`infra/k8s/` has Deployment + Service manifests for every component plus an
Ingress. To try it against a local cluster (kind or minikube):

```bash
# build images locally first, e.g.:
docker build -f services/auth/Dockerfile -t skillforge-auth:latest .
# (repeat for core, analyzer, ai, gateway; docker build -t skillforge-frontend:latest ./frontend)

kubectl apply -f infra/k8s/
kubectl create secret generic skillforge-secrets -n skillforge \
  --from-literal=JWT_SECRET=some-random-string \
  --from-literal=ANTHROPIC_API_KEY=your-key \
  --from-literal=POSTGRES_PASSWORD=skillforge \
  --dry-run=client -o yaml | kubectl apply -f -
```

## Submitting for PS-03

The submission checklist from the problem statement, and where each item is:

| Item | Location |
|---|---|
| GitHub repository | this repo (push it per instructions above) |
| Live application | Render deploy link (above) |
| Student dashboard | `frontend/src/pages/StudentDashboard.tsx` |
| Admin/mentor dashboard | `frontend/src/pages/MentorDashboard.tsx` |
| AI assistant | `services/ai/main.py` (`/chat`), used in the "AI assistant" tab |
| RAG knowledge base | `services/ai/rag.py`, `services/ai/seed_kb.py` |
| Agent implementation | `services/ai/agent.py` (career planning agent, 4 tools) |
| Python service | `services/analyzer/analyzer.py` (`SkillAnalyzer`, `SkillGapCalculator`, `RoadmapGenerator`) |
| API documentation | auto-generated Swagger UI per service at `/docs` (see table above) |
| Architecture diagram | `docs/architecture.md` |
| Docker files | one `Dockerfile` per service under `services/*/` and `frontend/` |
| Kubernetes manifests | `infra/k8s/` |
| Terraform files | `infra/terraform/` |
| Linux shell script | `scripts/setup.sh` |
| Database schema | `docs/db-schema.md` |
| Demo video | record yourself walking through the flow below — not something I can generate for you |
| Presentation | build from `docs/architecture.md` + this README — also not something I can generate here |
| README | this file |

## Demo flow (matches the required demo order)

1. Sign up (student)
2. Fill in profile: education, career goal
3. Add a couple of skills
4. Take an assessment (pick an area, e.g. Python)
5. View the roadmap tab → pick a target role → "Generate roadmap" → see
   skill gaps
6. Open the AI assistant tab → ask: *"I know Python and basic web
   development. I want to become an AI engineer. What should I learn next?"*
   (uses RAG)
7. Same tab, switch to "Career agent" mode → ask: *"Analyze my profile and
   tell me what I should learn next."* (uses the agent's tools)
8. Sign out, sign up again as a mentor → see the student you just created in
   the mentor dashboard
9. Point at `docker-compose.yml` / `infra/k8s/` / `infra/terraform/` to show
   the deployment/containerization pieces

## Known limitations (worth being upfront about)

- Shared Postgres database rather than one-per-service — see
  `docs/architecture.md` for the reasoning; this is a deliberate hackathon
  scope decision, not an oversight.
- No automated tests included — given the time budget, manual verification
  (documented in this build's process) took priority over a test suite. Add
  `pytest` tests under each service if you have time before submission.
- The AI service's embedding model downloads on first startup and needs
  normal internet access; it's cached after that.
