"""
Populates the Chroma knowledge base used for RAG.
Run once after Chroma is up: python -m services.ai.seed_kb
"""
from .rag import add_documents

KNOWLEDGE_BASE = [
    {
        "id": "res-python-1",
        "text": "Python fundamentals: variables, control flow, functions, data structures (lists, dicts, sets). "
                "Recommended for anyone starting a software career. Practice by solving small scripts before "
                "moving to OOP.",
        "metadata": {"topic": "python", "type": "resource"},
    },
    {
        "id": "res-python-2",
        "text": "Object-oriented Python: classes, inheritance, composition, dataclasses, and when to prefer "
                "composition over inheritance. Core for writing maintainable backend services.",
        "metadata": {"topic": "python", "type": "resource"},
    },
    {
        "id": "res-web-1",
        "text": "Web development roadmap: HTML/CSS/JS basics, then a frontend framework such as React, then REST "
                "API design and authentication. Build at least one full-stack CRUD project before applying for jobs.",
        "metadata": {"topic": "web_development", "type": "roadmap"},
    },
    {
        "id": "res-git-1",
        "text": "Git essentials: commits, branches, merging, and the pull-request workflow used on real engineering "
                "teams. Learn to resolve merge conflicts confidently before joining a team project.",
        "metadata": {"topic": "git", "type": "resource"},
    },
    {
        "id": "res-devops-1",
        "text": "DevOps roadmap: Linux shell scripting, Docker containers, CI/CD pipelines (GitHub Actions), then "
                "Kubernetes for orchestration. Terraform is used to provision cloud infrastructure as code.",
        "metadata": {"topic": "devops", "type": "roadmap"},
    },
    {
        "id": "res-ai-1",
        "text": "AI engineering roadmap: Python fluency, ML fundamentals, then applied LLM skills such as prompt "
                "engineering, retrieval-augmented generation (RAG), and building tool-using agents.",
        "metadata": {"topic": "ai", "type": "roadmap"},
    },
    {
        "id": "res-ai-2",
        "text": "Retrieval-augmented generation (RAG) grounds a language model's answers in a knowledge base by "
                "retrieving relevant documents before generation, reducing hallucination for domain-specific "
                "questions.",
        "metadata": {"topic": "ai", "type": "concept"},
    },
    {
        "id": "res-db-1",
        "text": "Database fundamentals: relational schema design, normalization, SQL joins and indexing. Learn "
                "PostgreSQL for structured data; learn a NoSQL store like MongoDB for flexible document data.",
        "metadata": {"topic": "database", "type": "resource"},
    },
    {
        "id": "role-ai-engineer",
        "text": "AI engineer target role: requires strong Python, applied AI/ML skills including RAG and agents, "
                "working database knowledge, and enough web development to ship a product around the model.",
        "metadata": {"topic": "ai", "type": "role"},
    },
    {
        "id": "role-backend",
        "text": "Backend developer target role: requires strong Python or another server language, deep database "
                "skills, REST/GraphQL API design, Git workflow fluency, and basic DevOps for deployment.",
        "metadata": {"topic": "database", "type": "role"},
    },
    {
        "id": "project-ai-1",
        "text": "Project idea for AI engineering: build a small RAG chatbot over your own class notes using a "
                "vector database and a hosted LLM API. Deploy it with a simple web frontend.",
        "metadata": {"topic": "ai", "type": "project"},
    },
    {
        "id": "project-web-1",
        "text": "Project idea for web development: build a full-stack task manager with user authentication, a "
                "REST API, and a React frontend, then deploy it publicly.",
        "metadata": {"topic": "web_development", "type": "project"},
    },
]


def run():
    add_documents(KNOWLEDGE_BASE)
    print(f"Seeded {len(KNOWLEDGE_BASE)} documents into the knowledge base.")


if __name__ == "__main__":
    run()
