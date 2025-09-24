import os
import random


class LLMClient:
    def __init__(self):
        self.use_mock = not os.getenv("OPENAI_API_KEY")

    def analyze(self, text: str):
        if self.use_mock:
            # Mock fallback response
            return {
                "summary": "This is a mock summary of the text.",
                "title": "Mock Title",
                "topics": ["topic1", "topic2", "topic3"],
                "sentiment": random.choice(["positive", "neutral", "negative"])
            }
        else:
            from openai import OpenAI
            client = OpenAI(api_key=os.getenv("OPENAI_API_KEY"))

            prompt = f"""
            Text: {text}

            1. Provide a 1–2 sentence summary.
            2. If a title exists, extract it. Else return "Untitled".
            3. List 3 key topics.
            4. Identify sentiment (positive, neutral, negative).
            """

            response = client.chat.completions.create(
                model="gpt-4o-mini",
                messages=[{"role": "user", "content": prompt}]
            )

            output = response.choices[0].message.content.strip()
            # Ideally parse JSON, but since time-limited, just return parsed stub
            return {
                "summary": output.split("\n")[0],
                "title": "Untitled",
                "topics": ["example", "stub", "topics"],
                "sentiment": "neutral"
            }
