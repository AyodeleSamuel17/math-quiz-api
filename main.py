from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json, random

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"], allow_credentials=True,
    allow_methods=["*"], allow_headers=["*"],
)

with open("large_questions_dataset.json") as f:
    questions = json.load(f)["questions"]

@app.get("/question")
def get_question(grade: str, topic: str, difficulty: str):
    matching = [q for q in questions if q["grade"] == grade and q["topic"] == topic and q["difficulty"] == difficulty]
    if not matching:
        raise HTTPException(status_code=404, detail="Not found")
    return random.choice(matching)
