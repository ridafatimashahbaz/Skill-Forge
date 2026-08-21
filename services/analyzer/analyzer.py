"""
Plain-Python OOP layer for SkillForge.

These classes contain no framework code so they can be unit tested and
reused directly by the AI agent's tools, in addition to being exposed
over HTTP by main.py.
"""
from dataclasses import dataclass, field
from typing import Dict, List


# Reference skill map per target role: topic -> importance weight (0-1)
ROLE_SKILL_MAP: Dict[str, Dict[str, float]] = {
    "ai_engineer": {
        "python": 1.0, "ai": 1.0, "database": 0.6, "web_development": 0.5,
        "git": 0.7, "devops": 0.5,
    },
    "backend_developer": {
        "python": 0.9, "database": 1.0, "web_development": 0.8,
        "git": 0.8, "devops": 0.6, "ai": 0.2,
    },
    "frontend_developer": {
        "web_development": 1.0, "git": 0.8, "python": 0.3,
        "database": 0.3, "devops": 0.3, "ai": 0.1,
    },
    "devops_engineer": {
        "devops": 1.0, "git": 0.9, "python": 0.6, "database": 0.5,
        "web_development": 0.3, "ai": 0.2,
    },
    "full_stack_developer": {
        "web_development": 1.0, "python": 0.7, "database": 0.8,
        "git": 0.8, "devops": 0.5, "ai": 0.3,
    },
}

# topic -> ordered list of recommended subtopics (used when a gap is found)
TOPIC_CURRICULUM: Dict[str, List[str]] = {
    "python": ["Python syntax & data structures", "OOP in Python", "Testing with pytest", "Async Python"],
    "ai": ["ML fundamentals", "Prompt engineering", "RAG systems", "Agentic AI & tool use"],
    "database": ["SQL fundamentals", "Relational schema design", "Indexing & query optimization", "NoSQL basics"],
    "web_development": ["HTML/CSS/JS fundamentals", "A frontend framework (React)", "REST API design", "Auth & sessions"],
    "git": ["Git basics (commit/branch/merge)", "Pull request workflow", "Rebasing & conflict resolution"],
    "devops": ["Linux shell scripting", "Docker fundamentals", "CI/CD pipelines", "Kubernetes basics"],
}


@dataclass
class SkillAnalyzer:
    """Turns raw assessment answers into a 0-100 score per area."""

    def calculate_score(self, correct_count: int, total_questions: int) -> float:
        if total_questions <= 0:
            return 0.0
        return round((correct_count / total_questions) * 100, 2)

    def score_all_areas(self, results: Dict[str, Dict[str, int]]) -> Dict[str, float]:
        """results: {area: {"correct": int, "total": int}}"""
        return {area: self.calculate_score(r["correct"], r["total"]) for area, r in results.items()}


@dataclass
class SkillGapCalculator:
    """Compares a student's current scores against a target role's requirements."""

    passing_threshold: float = 60.0

    def identify_gaps(self, scores: Dict[str, float], target_role: str) -> List[Dict]:
        role_weights = ROLE_SKILL_MAP.get(target_role, {})
        gaps = []
        for topic, weight in role_weights.items():
            current = scores.get(topic, 0.0)
            if current < self.passing_threshold and weight >= 0.4:
                gap_size = round((self.passing_threshold - current) * weight, 2)
                gaps.append({
                    "topic": topic,
                    "current_score": current,
                    "target_weight": weight,
                    "gap_size": gap_size,
                })
        gaps.sort(key=lambda g: g["gap_size"], reverse=True)
        return gaps


@dataclass
class RoadmapGenerator:
    """Builds a structured roadmap: current level -> gaps -> topics -> projects -> resources -> target role."""

    def recommend_topics(self, gaps: List[Dict]) -> List[Dict]:
        recommendations = []
        for gap in gaps:
            subtopics = TOPIC_CURRICULUM.get(gap["topic"], [])
            recommendations.append({
                "topic": gap["topic"],
                "priority": "high" if gap["gap_size"] > 30 else "medium",
                "subtopics": subtopics,
            })
        return recommendations

    def generate(self, current_level: str, scores: Dict[str, float], gaps: List[Dict],
                 target_role: str, projects: List[str], resources: List[Dict]) -> Dict:
        return {
            "current_level": current_level,
            "scores": scores,
            "skill_gaps": gaps,
            "recommended_topics": self.recommend_topics(gaps),
            "suggested_projects": projects,
            "resources": resources,
            "target_role": target_role,
        }


def suggest_projects_for_gaps(gaps: List[Dict]) -> List[str]:
    project_ideas = {
        "python": "Build a CLI tool that automates a repetitive task",
        "ai": "Build a small RAG chatbot over your own notes",
        "database": "Design and implement a normalized schema for a booking app",
        "web_development": "Build a full-stack CRUD app with auth",
        "git": "Contribute a PR to an open-source project",
        "devops": "Containerize an existing app and deploy it with CI/CD",
    }
    return [project_ideas[g["topic"]] for g in gaps if g["topic"] in project_ideas]
