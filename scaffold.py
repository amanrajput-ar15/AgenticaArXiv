import os
from pathlib import Path

dirs = [
    "backend/agenticarxiv/agents",
    "backend/agenticarxiv/ingestion",
    "backend/agenticarxiv/vectorstore",
    "backend/agenticarxiv/mcp",
    "backend/agenticarxiv/api",
    "frontend"
]

files = [
    "backend/agenticarxiv/__init__.py",
    "backend/agenticarxiv/agents/__init__.py",
    "backend/agenticarxiv/ingestion/__init__.py",
    "backend/main.py",
    "backend/worker.py",
    "backend/requirements.txt",
    "backend/.env",
    "backend/.env.example",
    "backend/nixpacks.toml",
    "backend/railway.toml",
    ".gitignore"
]

for d in dirs:
    os.makedirs(d, exist_ok=True)

for f in files:
    Path(f).touch()

print("Directory scaffolding complete.")