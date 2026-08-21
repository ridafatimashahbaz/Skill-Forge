# 🚀 SkillForge — AI-Powered Student Skills & Career Development Platform

> **Know your skills. Discover your gaps. Build the right projects. Become career-ready.**

SkillForge is an AI-powered student career development platform designed to help university students understand where they currently stand, identify missing skills, receive personalized learning recommendations, and build a practical roadmap toward their target career.

Instead of giving students generic course lists, SkillForge connects **skills → gaps → projects → learning → career readiness** in one platform.

---

## 🎯 Problem

Many students want careers in software engineering, AI, data science, cybersecurity, and other technology fields, but they often don't know:

- What skills their target career actually requires
- Which skills they already have
- Which skills they are missing
- What projects they should build
- What to learn next
- Whether they are actually job-ready
- How their university coursework connects to industry requirements

Students often spend months learning random technologies without a clear roadmap.

### 💡 SkillForge solves this by creating a personalized skill-to-career roadmap.

---

# 🌟 Key Features

## 🧠 AI-Powered Skill Gap Analysis

Students can provide their current skills, education, experience, and career goals.

SkillForge analyzes the profile and identifies:

- Current strengths
- Missing skills
- Skill priorities
- Recommended next steps
- Career readiness areas

---

## 🎯 Career Goal Mapping

Students can select a target career such as:

- Software Engineer
- Full-Stack Developer
- AI/ML Engineer
- Data Scientist
- Data Analyst
- Cybersecurity Engineer
- Cloud Engineer
- DevOps Engineer

The platform maps the selected career to the skills required to pursue it.

---

## 📊 Personalized Skill Roadmap

Instead of giving every student the same learning path, SkillForge generates a roadmap based on their current level.

Example:

```text
Current Skills
      ↓
Skill Assessment
      ↓
Skill Gap Analysis
      ↓
Priority Skills
      ↓
Learning Roadmap
      ↓
Project Recommendations
      ↓
Career Readiness
🛠️ Project Recommendations

SkillForge recommends practical projects that students can build to demonstrate their skills.

Projects are selected according to:

Target career
Current skill level
Missing skills
Learning objectives

This helps students turn theoretical knowledge into portfolio-ready work.

🤖 AI Career Assistant

The AI assistant provides personalized guidance for questions such as:

"What should I learn after Java?"

"Which projects should I build for an AI internship?"

"What skills am I missing for a full-stack developer role?"

"How can I become internship-ready?"

The assistant uses the student's profile and SkillForge's knowledge base to provide contextual recommendations.

📚 AI + RAG Knowledge Base

SkillForge uses Retrieval-Augmented Generation (RAG) to provide more relevant career and learning recommendations.

The system combines:

Student profile data
Career skill requirements
Learning resources
Project knowledge
AI reasoning

with a vector knowledge base powered by ChromaDB.

🏗️ System Architecture
                         ┌─────────────────────┐
                         │      Frontend       │
                         │    React + Vite     │
                         └──────────┬──────────┘
                                    │
                                    ▼
                         ┌─────────────────────┐
                         │       Gateway       │
                         │       Nginx         │
                         └──────────┬──────────┘
                                    │
              ┌─────────────────────┼─────────────────────┐
              │                     │                     │
              ▼                     ▼                     ▼
       ┌────────────┐       ┌────────────┐       ┌────────────┐
       │    Auth    │       │    Core    │       │  Analyzer  │
       │  Service   │       │  Service   │       │  Service   │
       └─────┬──────┘       └─────┬──────┘       └─────┬──────┘
             │                    │                    │
             └────────────────────┼────────────────────┘
                                  ▼
                         ┌─────────────────┐
                         │   PostgreSQL    │
                         │    Database     │
                         └─────────────────┘


                                  │
                                  ▼
                         ┌─────────────────┐
                         │   AI Service    │
                         │  Claude + RAG   │
                         └────────┬────────┘
                                  │
                                  ▼
                         ┌─────────────────┐
                         │    ChromaDB     │
                         │ Vector Database  │
                         └─────────────────┘
🧩 Technology Stack
Frontend
React
Vite
JavaScript / JSX
Tailwind CSS
React Router
Backend
Python
FastAPI
Uvicorn
REST APIs
Database
PostgreSQL
AI
Anthropic Claude
Retrieval-Augmented Generation (RAG)
ChromaDB
Vector embeddings
Infrastructure
Docker
Docker Compose
Nginx
GitHub
Deployment
Vercel — frontend
Docker-based deployment architecture for backend services
📁 Project Structure
skillforge/
│
├── frontend/
│   ├── src/
│   ├── public/
│   ├── Dockerfile
│   ├── nginx.conf
│   └── package.json
│
├── services/
│   │
│   ├── auth/
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── core/
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── analyzer/
│   │   ├── main.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── ai/
│   │   ├── main.py
│   │   ├── rag.py
│   │   ├── seed_kb.py
│   │   ├── Dockerfile
│   │   └── requirements.txt
│   │
│   ├── gateway/
│   │   ├── nginx.conf
│   │   └── Dockerfile
│   │
│   └── common/
│
├── docs/
│
├── scripts/
│
├── infra/
│
├── docker-compose.yml
├── render.yaml
├── .env.example
└── README.md
🔐 Authentication

SkillForge includes an authentication service responsible for:

User registration
Login
JWT-based authentication
Secure API authorization
User-specific career data

Authentication is separated into its own backend service to keep the architecture modular and scalable.

🤖 AI Workflow

The AI pipeline follows this process:

Student Profile
      ↓
Career Goal
      ↓
Skill Analysis
      ↓
Skill Gap Identification
      ↓
Knowledge Retrieval
      ↓
AI Reasoning
      ↓
Personalized Recommendations
      ↓
Learning + Project Roadmap

This allows SkillForge to provide recommendations based on the student's actual situation rather than generic career advice.

📈 Example Use Case
Student

A student wants to become a:

Full-Stack Developer

Current skills:

HTML
CSS
Java
Basic JavaScript

SkillForge identifies missing areas such as:

Advanced JavaScript
React
REST APIs
Backend Development
Databases
Git/GitHub
Deployment

The platform then generates a prioritized roadmap:

1. Strengthen JavaScript
        ↓
2. Learn React
        ↓
3. Learn REST APIs
        ↓
4. Build Full-Stack Project
        ↓
5. Learn Deployment
        ↓
6. Build Portfolio
        ↓
7. Internship Preparation
🌍 Sustainable Development Goals

SkillForge contributes to multiple United Nations Sustainable Development Goals.

🎓 SDG 4 — Quality Education

Provides personalized and accessible learning guidance for students.

💼 SDG 8 — Decent Work & Economic Growth

Helps students become more employable and career-ready.

💡 SDG 9 — Industry, Innovation & Infrastructure

Uses AI and modern software infrastructure to improve career development.

🤝 SDG 10 — Reduced Inequalities

Provides structured career guidance to students who may not have access to professional mentorship.

🚀 Getting Started
Prerequisites

Install:

Git
Docker
Docker Compose

An Anthropic API key is required for AI functionality.

1. Clone the repository
git clone https://github.com/ridafatimashahbaz/skillforge.git
cd skillforge
2. Configure environment variables

Copy the example environment file:

cp .env.example .env

Add your API configuration:

ANTHROPIC_API_KEY=your_api_key
ANTHROPIC_MODEL=claude-sonnet-4-6
JWT_SECRET=your_secure_secret
3. Start SkillForge
docker compose up --build

The main services will start through Docker Compose.

4. Access the application

Frontend:

http://localhost:3000

Gateway:

http://localhost:8080
🧪 Development

Run the frontend separately:

cd frontend
npm install
npm run dev

The development server runs on:

http://localhost:5173
🔌 Backend Services
Service	Purpose
Auth	Authentication & JWT
Core	Student and career data
Analyzer	Skill gap analysis
AI	AI recommendations & RAG
ChromaDB	Vector knowledge base
Gateway	API routing
PostgreSQL	Persistent data storage
Frontend	User interface
🛡️ Security

The project uses:

JWT authentication
Environment variables for secrets
Separate backend services
Docker-based isolation
API gateway routing
No secrets committed to GitHub

Never commit .env or API keys to the repository.

📊 Why SkillForge?

Traditional career platforms often answer:

"Here are courses you can take."

SkillForge aims to answer:

"Here is where you are, here is where you need to be, and here is exactly what you should do next."

The platform transforms career development from a collection of disconnected resources into a personalized, measurable roadmap.

🔮 Future Improvements

Planned improvements include:

📄 AI-powered resume analysis
💼 Internship and job matching
🔗 LinkedIn profile analysis
📊 Skill progress tracking
🏆 Gamified learning
🎓 University curriculum mapping
🧑‍💼 Mentor matching
📈 Industry demand analytics
🧪 Automated project evaluation
🎤 AI-powered interview preparation
🏆 Hackathon Project

Project: SkillForge
Category: AI / Education / Career Development

Relevant SDGs
SDG 4 — Quality Education
SDG 8 — Decent Work & Economic Growth
SDG 9 — Industry, Innovation & Infrastructure
SDG 10 — Reduced Inequalities
🔗 Project Links
GitHub Repository

https://github.com/ridafatimashahbaz/skillforge

Live Application

https://skillforge-woad-seven.vercel.app/

👩‍💻 Team

Built as an AI-powered solution for student career development.

⭐ Support

If you find SkillForge useful, consider giving the repository a ⭐ on GitHub.
