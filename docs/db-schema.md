# Database schema

All tables live in one PostgreSQL database (`skillforge`), shared by the Auth,
Core, and Analyzer services. Each service only touches the tables it owns;
sharing one database keeps the hackathon build simple while the service
boundary is still enforced in code (each service exposes its own API).

| Table | Owned by | Purpose |
|---|---|---|
| `users` | Auth | Login credentials, role (student/mentor/admin) |
| `profiles` | Core | One-to-one with `users`; education, career goal, experience level, optional `mentor_id` |
| `skills` | Core | Self-rated skills per profile (name, proficiency 1-5) |
| `projects` | Core | Portfolio projects per profile |
| `certifications` | Core | Certifications per profile |
| `assessment_questions` | Analyzer | Multiple-choice question bank per area (python, web_development, git, devops, ai, database) |
| `assessments` | Analyzer | A profile's score for one area at one point in time |
| `roadmaps` | Analyzer | Generated roadmap snapshots (JSON blob) per profile |
| `learning_resources` | AI (via Core's DB access, or Chroma) | Structured resource records; the RAG knowledge base itself lives in Chroma, not Postgres |

## Key relationships

```
users (1) ──── (1) profiles
profiles (1) ──── (*) skills
profiles (1) ──── (*) projects
profiles (1) ──── (*) certifications
profiles (1) ──── (*) assessments
profiles (1) ──── (*) roadmaps
users (1, as mentor) ──── (*) profiles.mentor_id
```

`profiles` has two foreign keys into `users` (`user_id` for the owning
student, `mentor_id` for an assigned mentor) — both relationships specify
`foreign_keys` explicitly in SQLAlchemy since a table with two FKs to the same
parent table is otherwise ambiguous.

## Notes

- IDs are UUIDs (string form) generated in application code, not
  auto-increment integers — this keeps IDs safe to expose in URLs.
- `roadmaps.content_json` stores the full generated roadmap (current level,
  gaps, recommended topics, projects, resources) as JSON rather than
  normalizing it further — it's a point-in-time snapshot, not something the
  app queries by field.
- The RAG knowledge base (learning resources, roadmaps, course info used for
  grounding) is stored as embedded documents in Chroma, not Postgres, since
  it's queried by semantic similarity rather than exact match.
