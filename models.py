from pydantic import BaseModel
from typing import List

class AnalyzeRequest(BaseModel):
    text: str

class AnalyzeResponse(BaseModel):
    summary: str
    title: str
    topics: List[str]
    sentiment: str
    keywords: List[str]
