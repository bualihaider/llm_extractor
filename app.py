from fastapi import FastAPI, HTTPException
from db import init_db, get_db
from llm import LLMClient
from nlp import extract_keywords
from models import AnalyzeRequest, AnalyzeResponse
import json

app = FastAPI(title="LLM Knowledge Extractor")
init_db()
llm = LLMClient()

@app.post("/analyze", response_model=AnalyzeResponse)
def analyze(request: AnalyzeRequest):
    if not request.text.strip():
        raise HTTPException(status_code=400, detail="Input text is empty.")

    try:
        llm_result = llm.analyze(request.text)
        keywords = extract_keywords(request.text)

        data = {
            "summary": llm_result["summary"],
            "title": llm_result["title"],
            "topics": llm_result["topics"],
            "sentiment": llm_result["sentiment"],
            "keywords": keywords,
        }

        with get_db() as conn:
            conn.execute(
                "INSERT INTO analyses (text, summary, title, topics, sentiment, keywords) VALUES (?, ?, ?, ?, ?, ?)",
                (request.text, data["summary"], data["title"], json.dumps(data["topics"]), data["sentiment"], json.dumps(data["keywords"]))
            )
            conn.commit()

        return data
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"LLM processing failed: {e}")

@app.get("/search")
def search(topic: str):
    with get_db() as conn:
        cursor = conn.execute("SELECT id, text, summary, title, topics, sentiment, keywords FROM analyses")
        rows = cursor.fetchall()

    results = []
    for row in rows:
        topics = json.loads(row[4])
        keywords = json.loads(row[6])
        if topic in topics or topic in keywords:
            results.append({
                "id": row[0],
                "text": row[1],
                "summary": row[2],
                "title": row[3],
                "topics": topics,
                "sentiment": row[5],
                "keywords": keywords
            })

    return {"results": results}
