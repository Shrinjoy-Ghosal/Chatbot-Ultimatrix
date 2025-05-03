from fastapi import FastAPI
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

app = FastAPI()

class ChatbotRequest(BaseModel):
    query: str

async def google_search(query: str) -> str:
    """Fetches detailed search results from Google Custom Search API."""
    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"
    response = requests.get(url)
    
    items = response.json().get("items", [])
    detailed_response = ""

    # Fetch multiple search results instead of just one
    for item in items[:3]:  # Increase the number for longer responses
        snippet = item.get("snippet", "No additional details.")
        title = item.get("title", "Untitled")
        link = item.get("link", "No link")
        detailed_response += f"🔹 **{title}**\n{snippet}\n🔗 [More Info]({link})\n\n"

    return detailed_response if detailed_response else "No relevant information found."

@app.post("/chatbot")
async def chatbot(request: ChatbotRequest):
    return {"answer": await google_search(request.query)}