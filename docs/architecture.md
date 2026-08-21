# Architecture

```
                        ┌─────────────────┐
                        │  React frontend  │
                        │  (Vite, Tailwind)│
                        └────────┬─────────┘
                                 │  HTTPS
                        ┌────────▼─────────┐
                        │   API Gateway     │
                        │  (Nginx reverse   │
                        │      proxy)       │
                        └───┬───┬───┬───┬───┘
              ┌─────────────┘   │   │   └─────────────┐
              ▼                 ▼   ▼                  ▼
        ┌──────────┐    ┌──────────┐ ┌──────────┐ ┌──────────┐
        │   Auth   │    │   Core   │ │ Analyzer │ │    AI    │
        │ service  │    │ service  │ │ service  │ │ service  │
        │  (JWT)   │    │ (profile)│ │  (score, │ │ (RAG +   │
        │          │    │          │ │  roadmap)│ │  agent)  │
        └────┬─────┘    └────┬─────┘ └────┬─────┘ └────┬─────┘
             │                │            │            │
             └────────┬───────┴────────────┘            │
                       ▼                                 ▼
              ┌─────────────────┐                ┌───────────────┐
              │   PostgreSQL     │                │  Chroma       │
              │ (users, profiles,│                │ (vector store,│
              │  skills, scores) │                │  RAG docs)    │
              └─────────────────┘                └───────────────┘
```

The AI service also calls the Core and Analyzer services directly
(server-to-server, still JWT-authenticated) when the career agent needs to
look up a student's skills or compute a gap analysis — see "Agent tools"
below.

## Services

| Service | Responsibility | Tech |
|---|---|---|
| Gateway | Single entry point; routes `/auth`, `/core`, `/analyzer`, `/ai` to the right backend | Nginx |
| Auth | Signup, login, JWT issuance, role storage | FastAPI, SQLAlchemy, Postgres |
| Core | Profile, skills, projects, certifications; mentor/admin student views; RBAC | FastAPI, SQLAlchemy, Postgres |
| Analyzer | Assessment questions/scoring, gap analysis, roadmap generation | FastAPI + plain-Python `SkillAnalyzer`/`SkillGapCalculator`/`RoadmapGenerator` classes |
| AI | RAG chat grounded in the knowledge base; agentic career-planning assistant with tool use | FastAPI, Chroma, Anthropic API |
| Frontend | Student and mentor/admin dashboards | React, Vite, Tailwind |

## Agent tools

The career-planning agent (`services/ai/agent.py`) is given four tools and
decides which to call based on the student's message:

1. `analyze_student_skills` — calls Core's `/profile/me`
2. `generate_skill_gap` — calls Analyzer's internal gap-analysis endpoint
3. `search_learning_resources` — semantic search over the Chroma knowledge base
4. `create_roadmap` — calls Analyzer's `/roadmap/generate` and persists the result

This keeps recommendations grounded: the agent is instructed to call
`search_learning_resources` rather than inventing resources, and to check the
student's actual skills/gaps before recommending anything specific.

## Why one Postgres database instead of one-per-service

Textbook microservices give each service its own database. For a hackathon
build, one shared Postgres instance with clear per-service table ownership
(see `docs/db-schema.md`) gets the same demo-able result with far less
operational overhead — no cross-database joins to fake, no data-sync problem
between services. The service boundary is enforced by each service only
exposing its own HTTP API, not by database isolation.

## Deployment topologies

- **Local (`docker-compose.yml`)**: every service is one container; Postgres
  and Chroma are also containers with named volumes for persistence.
- **Render (`render.yaml`)**: same shape, but Postgres is Render's managed
  database, and `auth`/`core`/`analyzer`/`ai`/`chroma` are private services
  reachable only from `gateway` and each other — `gateway` and `frontend` are
  the only two publicly reachable services.
- **Kubernetes (`infra/k8s/`)**: one Deployment + Service per component,
  matching the same shape again, plus an Ingress in front of `gateway` and
  `frontend`. These manifests are a submission deliverable; running them
  against a real cluster is optional for the demo (see main README).
