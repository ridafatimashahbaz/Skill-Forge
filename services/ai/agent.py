import os
import json
import httpx
from anthropic import Anthropic

from .rag import search as rag_search

CORE_SERVICE_URL = os.getenv("CORE_SERVICE_URL", "http://core:8000")
ANALYZER_SERVICE_URL = os.getenv("ANALYZER_SERVICE_URL", "http://analyzer:8000")
MODEL = os.getenv("ANTHROPIC_MODEL", "claude-sonnet-4-6")

client = Anthropic(api_key=os.getenv("ANTHROPIC_API_KEY"))

TOOLS = [
    {
        "name": "analyze_student_skills",
        "description": "Fetch the current student's profile: skills, experience level, career goal, projects.",
        "input_schema": {"type": "object", "properties": {}},
    },
    {
        "name": "generate_skill_gap",
        "description": "Compute the gap between the student's current assessed scores and a target role's "
                        "requirements. Returns per-topic gap sizes.",
        "input_schema": {
            "type": "object",
            "properties": {
                "target_role": {
                    "type": "string",
                    "description": "One of: ai_engineer, backend_developer, frontend_developer, "
                                    "devops_engineer, full_stack_developer",
                }
            },
            "required": ["target_role"],
        },
    },
    {
        "name": "search_learning_resources",
        "description": "Search the grounded knowledge base for learning resources, roadmaps, course info, "
                        "or project ideas relevant to a topic.",
        "input_schema": {
            "type": "object",
            "properties": {
                "query": {"type": "string", "description": "Search query, e.g. 'RAG systems for beginners'"},
                "topic": {
                    "type": "string",
                    "description": "Optional filter: python, web_development, git, devops, ai, database",
                },
            },
            "required": ["query"],
        },
    },
    {
        "name": "create_roadmap",
        "description": "Generate a full career roadmap (current level, gaps, topics, projects, resources) for "
                        "a target role, and persist it to the student's account.",
        "input_schema": {
            "type": "object",
            "properties": {
                "target_role": {"type": "string"},
            },
            "required": ["target_role"],
        },
    },
]

SYSTEM_PROMPT = (
    "You are the SkillForge Career Planning Agent. You help students figure out what to learn next to reach "
    "a target tech career. Always ground concrete recommendations in the search_learning_resources tool rather "
    "than inventing resources. Use analyze_student_skills and generate_skill_gap before recommending anything "
    "specific to the student. Be direct and concrete: name actual topics and next steps, not generic advice."
)


class CareerAgent:
    def __init__(self, user_token: str):
        self.user_token = user_token
        self.headers = {"Authorization": f"Bearer {user_token}"}

    # ---- tool implementations ----

    def _get_user_id(self) -> str:
        import jwt
        payload = jwt.decode(self.user_token, options={"verify_signature": False})
        return payload["sub"]

    def analyze_student_skills(self) -> dict:
        with httpx.Client() as c:
            r = c.get(f"{CORE_SERVICE_URL}/profile/me", headers=self.headers, timeout=10)
            r.raise_for_status()
            return r.json()

    def generate_skill_gap(self, target_role: str) -> dict:
        user_id = self._get_user_id()
        with httpx.Client() as c:
            r = c.get(
                f"{ANALYZER_SERVICE_URL}/internal/gap-analysis/{user_id}",
                params={"target_role": target_role},
                headers=self.headers,
                timeout=10,
            )
            r.raise_for_status()
            return r.json()

    def search_learning_resources(self, query: str, topic: str | None = None) -> dict:
        hits = rag_search(query, n_results=4, topic_filter=topic)
        return {"results": hits}

    def create_roadmap(self, target_role: str) -> dict:
        with httpx.Client() as c:
            r = c.post(
                f"{ANALYZER_SERVICE_URL}/roadmap/generate",
                json={"target_role": target_role},
                headers=self.headers,
                timeout=10,
            )
            r.raise_for_status()
            return r.json()

    def _dispatch(self, tool_name: str, tool_input: dict) -> dict:
        fn = getattr(self, tool_name, None)
        if fn is None:
            return {"error": f"unknown tool {tool_name}"}
        try:
            return fn(**tool_input)
        except Exception as e:
            return {"error": str(e)}

    # ---- main loop ----

    def run(self, user_message: str, history: list[dict] | None = None, max_turns: int = 5) -> dict:
        messages = list(history or [])
        messages.append({"role": "user", "content": user_message})

        tool_trace = []

        for _ in range(max_turns):
            response = client.messages.create(
                model=MODEL,
                max_tokens=1500,
                system=SYSTEM_PROMPT,
                tools=TOOLS,
                messages=messages,
            )

            if response.stop_reason != "tool_use":
                final_text = "".join(b.text for b in response.content if b.type == "text")
                messages.append({"role": "assistant", "content": response.content})
                return {"reply": final_text, "messages": messages, "tool_trace": tool_trace}

            messages.append({"role": "assistant", "content": response.content})

            tool_results = []
            for block in response.content:
                if block.type != "tool_use":
                    continue
                result = self._dispatch(block.name, block.input)
                tool_trace.append({"tool": block.name, "input": block.input, "output": result})
                tool_results.append({
                    "type": "tool_result",
                    "tool_use_id": block.id,
                    "content": json.dumps(result),
                })

            messages.append({"role": "user", "content": tool_results})

        return {"reply": "I wasn't able to finish that within the tool-call budget — try a narrower question.",
                "messages": messages, "tool_trace": tool_trace}
