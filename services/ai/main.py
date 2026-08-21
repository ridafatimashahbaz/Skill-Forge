import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), "..", ".."))

from fastapi import FastAPI, Depends, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.security import HTTPAuthorizationCredentials
from pydantic import BaseModel
from anthropic import Anthropic

from services.common.deps import get_current_claims, bearer_scheme
from .rag import search as rag_search
from .agent import CareerAgent

app = FastAPI(title="SkillForge AI Service")
app.add_middleware(CORSMiddleware, allow_origins=["*"], allow_methods=["*"], allow_headers=["*"])

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")


@app.get("/health")
def health():
    return {"status": "ok", "service": "ai"}


# ---------- Plain RAG chat ----------

class ChatRequest(BaseModel):
    message: str


@app.post("/chat")
def chat(payload: ChatRequest, claims: dict = Depends(get_current_claims)):
    hits = rag_search(payload.message, n_results=4)
    context = "\n\n".join(f"- {h['text']}" for h in hits)

    system = (
        "You are the SkillForge career assistant. Answer the student's question using only the provided "
        "knowledge base context. If the context doesn't cover it, say so plainly instead of guessing."
    )
    prompt = f"Knowledge base context:\n{context}\n\nStudent question: {payload.message}"

    response = client.messages.create(
        model=MODEL,
        max_tokens=800,
        system=system,
        messages=[{"role": "user", "content": prompt}],
    )
    text = "".join(b.text for b in response.content if b.type == "text")
    return {"reply": text, "sources": hits}


# ---------- Agentic career planning ----------

class AgentRequest(BaseModel):
    message: str


@app.post("/agent")
def run_agent(
    payload: AgentRequest,
    claims: dict = Depends(get_current_claims),
    creds: HTTPAuthorizationCredentials = Depends(bearer_scheme),
):
    agent = CareerAgent(user_token=creds.credentials)
    result = agent.run(payload.message)
    return {"reply": result["reply"], "tool_trace": result["tool_trace"]}
