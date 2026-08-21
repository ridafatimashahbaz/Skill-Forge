"""
Seeds the assessment_questions table with a small starter bank covering
Python, Web Development, Git, DevOps, AI, and Database.
Run from repo root: python scripts/seed_questions.py
"""
import sys, os
sys.path.append(os.path.join(os.path.dirname(__file__), ".."))

from services.common.db import Base, engine, SessionLocal
from services.common.models import AssessmentQuestion

QUESTIONS = [
    ("python", "What does `len([1,2,3])` return?", "2", "3", "1", "Error", "b", 1),
    ("python", "Which keyword defines a function in Python?", "func", "def", "function", "lambda", "b", 1),
    ("python", "What is the output of `type([])` in Python?", "list", "<class 'list'>", "array", "tuple", "b", 1),
    ("python", "Which of these creates a class in Python?", "class Foo:", "def Foo():", "new Foo()", "struct Foo:", "a", 1),
    ("python", "What does a Python decorator do?", "Deletes a function", "Wraps/extends a function's behavior", "Imports a module", "Compiles code", "b", 2),

    ("web_development", "Which HTTP method is idempotent and used to fully replace a resource?", "POST", "PUT", "PATCH", "CONNECT", "b", 2),
    ("web_development", "What does CSS stand for?", "Cascading Style Sheets", "Computer Style Sheets", "Creative Style System", "Colorful Style Sheets", "a", 1),
    ("web_development", "In React, what hook manages local component state?", "useEffect", "useState", "useRef", "useMemo", "b", 1),
    ("web_development", "Which status code means 'Not Found'?", "200", "301", "404", "500", "c", 1),
    ("web_development", "What does REST stand for?", "Representational State Transfer", "Remote State Transfer", "Real-time State Transfer", "Recursive State Transfer", "a", 2),

    ("git", "Which command creates a new branch and switches to it?", "git branch -m", "git checkout -b", "git switch --new", "git commit -b", "b", 1),
    ("git", "What does `git merge` do?", "Deletes a branch", "Combines changes from one branch into another", "Reverts a commit", "Clones a repo", "b", 1),
    ("git", "What is a 'merge conflict'?", "A bug in Git itself", "Overlapping changes Git can't auto-resolve", "A failed push", "A deleted branch", "b", 2),
    ("git", "Which command shows commit history?", "git log", "git show", "git history", "git diff", "a", 1),

    ("devops", "What does Docker package an application into?", "A virtual machine", "A container", "A database", "A repository", "b", 1),
    ("devops", "What is the purpose of a CI/CD pipeline?", "Style code automatically", "Automate build, test, and deployment", "Encrypt source code", "Manage DNS", "b", 2),
    ("devops", "What does Kubernetes primarily manage?", "Container orchestration", "Code compilation", "Database backups", "DNS routing", "a", 2),
    ("devops", "What is Terraform used for?", "Writing unit tests", "Infrastructure as code", "Frontend styling", "Log aggregation", "b", 2),

    ("ai", "What does RAG stand for in the context of LLMs?", "Rapid Answer Generation", "Retrieval-Augmented Generation", "Random Access Graph", "Recursive AI Gateway", "b", 2),
    ("ai", "What is a 'prompt' in the context of LLMs?", "A model's weights", "The input text given to a model", "A training dataset", "A GPU instruction", "b", 1),
    ("ai", "What does an AI 'agent' typically add beyond a plain chatbot?", "Bigger context window", "Ability to call tools/take actions", "Faster inference", "Lower cost", "b", 2),
    ("ai", "What is 'overfitting' in machine learning?", "Model performs well on training but poorly on new data", "Model trains too fast", "Model uses too little data", "Model has too few parameters", "a", 2),

    ("database", "What does SQL stand for?", "Structured Query Language", "Simple Query Logic", "Sequential Query Language", "System Query Language", "a", 1),
    ("database", "What is a primary key?", "A column that can repeat values", "A unique identifier for a row", "An index on all columns", "A foreign table reference", "b", 1),
    ("database", "What does a JOIN do in SQL?", "Deletes rows", "Combines rows from two or more tables", "Creates a new database", "Backs up a table", "b", 1),
    ("database", "What is database normalization mainly used for?", "Speeding up backups", "Reducing data redundancy", "Encrypting data", "Compressing storage", "b", 2),
]


def run():
    Base.metadata.create_all(bind=engine)
    db = SessionLocal()
    try:
        existing = db.query(AssessmentQuestion).count()
        if existing > 0:
            print(f"Questions already seeded ({existing} rows). Skipping.")
            return
        for area, q, a, b, c, d, correct, diff in QUESTIONS:
            db.add(AssessmentQuestion(
                area=area, question=q, option_a=a, option_b=b, option_c=c, option_d=d,
                correct_option=correct, difficulty=diff,
            ))
        db.commit()
        print(f"Seeded {len(QUESTIONS)} assessment questions.")
    finally:
        db.close()


if __name__ == "__main__":
    run()
