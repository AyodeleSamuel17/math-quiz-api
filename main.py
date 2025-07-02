from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
import json
import random
import os
import uvicorn

app = FastAPI()

# Enable CORS so your Unity app can access the API
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # You can restrict this to your Unity domain later
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Load questions from JSON file
with open("large_questions_dataset.json", "r") as f:
    data = json.load(f)
    questions = data["questions"]

@app.get("/question")
def get_question(grade: str, topic: str, difficulty: str):
    # Filter questions based on query
    filtered = [
        q for q in questions
        if q["grade"] == grade and q["topic"].lower() == topic.lower() and q["difficulty"].lower() == difficulty.lower()
    ]

    if not filtered:
        raise HTTPException(status_code=404, detail="No matching questions found")

    question = random.choice(filtered)
    return {
        "prompt": question["prompt"],
        "choices": question["choices"],
        "answer": question["answer"]
    }

if __name__ == "__main__":
    port = int(os.environ.get("PORT", 8000))  # Render uses PORT env variable
    uvicorn.run(app, host="0.0.0.0", port=port)
