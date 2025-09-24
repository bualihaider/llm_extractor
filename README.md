# 📖 LLM Knowledge Extractor

A small prototype system that takes unstructured text input and uses an LLM (or mock fallback) to produce:
- Structured metadata (`title`, `topics`, `sentiment`, `keywords`)
- Stores results in a lightweight database (SQLite)
- Provides an API for analysis and search

---

## 🚀 Features
- **POST /analyze** → Analyze new text, extract summary + metadata, persist in DB.
- **GET /search?topic=xyz** → Search stored analyses by topic or keyword.
- **Keyword Extraction** → Extracts 3 most frequent nouns using NLTK (not via LLM).
- **Robustness**:
  - Handles empty input
  - Graceful fallback to mock mode if LLM API fails or no API key is set

---

## 🛠️ Tech Stack
- **Backend**: [FastAPI](https://fastapi.tiangolo.com/)
- **Database**: SQLite (via Python’s built-in `sqlite3`)
- **LLM**: OpenAI API (with mock fallback)
- **NLP**: NLTK (for keyword extraction)

---

## 📂 Project Structure
llm_extractor/
├── app.py # FastAPI entrypoint
├── db.py # SQLite setup
├── llm.py # LLM wrapper (OpenAI + mock fallback)
├── nlp.py # Keyword extractor
├── models.py # Pydantic request/response models
└── requirements.txt


---

## ⚙️ Setup

### 1. Clone the repo
```bash
git clone https://github.com/your-username/llm-extractor.git
cd llm-extractor
```
### 2. Create a virtual environment (recommended)
```
python3 -m venv venv
source venv/bin/activate   # Linux/macOS
.\venv\Scripts\activate    # Windows
```
## 3. Install dependencies
```
pip install -r requirements.txt
```

## 4. Install NLTK resources
```
python -m nltk.downloader punkt averaged_perceptron_tagger_eng stopwords
```
## 5. (Optional) Add OpenAI API key
```
export OPENAI_API_KEY=your_api_key   # macOS/Linux
setx OPENAI_API_KEY "your_api_key"   # Windows
```

If no key is provided, the system runs in mock mode.

▶️ Running the App
```
uvicorn app:app --reload
```

API will be live at:
👉 http://127.0.0.1:8000/docs
 (Swagger UI)
👉 http://127.0.0.1:8000/redoc

📌 API Endpoints
POST /analyze

Analyze new text, extract summary & metadata, store in DB.

Request
```

{
  "text": "OpenAI released a new AI model today, which is expected to transform industries."
}
```

Response
```
{
  "summary": "OpenAI released a new AI model expected to transform industries.",
  "title": "Untitled",
  "topics": ["AI", "OpenAI", "industry"],
  "sentiment": "positive",
  "keywords": ["model", "industries", "ai"]
}
```
GET /search?topic=xyz

Search analyses by topic or keyword.

Example

GET /search?topic=AI


Response
```
{
  "results": [
    {
      "id": 1,
      "text": "OpenAI released a new AI model today...",
      "summary": "OpenAI released a new AI model expected to transform industries.",
      "title": "Untitled",
      "topics": ["AI", "OpenAI", "industry"],
      "sentiment": "positive",
      "keywords": ["model", "industries", "ai"]
    }
  ]
}
```
🧪 Edge Cases

Empty input → Returns 400 Bad Request

LLM API failure or no API key → Falls back to mock mode instead of crashing
