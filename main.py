from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
import json
import random

app = FastAPI()

# Allow all origins (for Unity or other clients)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load questions once at startup
with open("large_questions_dataset.json", "r") as f:
    data = json.load(f)
    questions = data["questions"]

@app.get("/question")
def get_question(grade: str, topic: str, difficulty: str):
    filtered = [
        q for q in questions
        if q["grade"] == grade and q["topic"].lower() == topic.lower() and q["difficulty"].lower() == difficulty.lower()
    ]
    if not filtered:
        return {"error": "No question found for given criteria"}
    return random.choice(filtered)

