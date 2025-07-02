from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import os
import uvicorn

app = FastAPI()

# Enable CORS for Unity
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Later replace "*" with your game domain
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load questions from JSON
with open("large_clean_questions_dataset_v2.json", "r") as f:
    data = json.load(f)
    questions = data["questions"]

@app.get("/question")
def get_question(grade: str, topic: str, difficulty: str):
    filtered = [
        q for q in questions
        if q.get("grade") == grade
        and q.get("topic", "").lower() == topic.lower()
        and q.get("difficulty", "").lower() == difficulty.lower()
    ]

    if not filtered:
        raise HTTPException(status_code=404, detail="No matching questions found")

    question = random.choice(filtered)

    return {
        "prompt": question.get("prompt"),
        "choices": question.get("choices", []),
        "answer": question.get("answer")
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))
    uvicorn.run(app, host="0.0.0.0", port=port)
