from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel
import requests
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

GOOGLE_API_KEY = os.getenv("GOOGLE_API_KEY")
SEARCH_ENGINE_ID = os.getenv("SEARCH_ENGINE_ID")

# Initialize FastAPI app
app = FastAPI()

# ✅ Enable CORS (Allows Frontend to Access Backend API)
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Adjust for security if needed
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

class ChatbotRequest(BaseModel):
    query: str

async def google_search(query: str) -> str:
    """Fetches detailed search results from Google Custom Search API."""
    if not GOOGLE_API_KEY or not SEARCH_ENGINE_ID:
        raise HTTPException(status_code=500, detail="Missing Google API credentials!")

    url = f"https://www.googleapis.com/customsearch/v1?key={GOOGLE_API_KEY}&cx={SEARCH_ENGINE_ID}&q={query}"

    try:
        response = requests.get(url)
        response.raise_for_status()  # Raises an error if request fails
    except requests.exceptions.RequestException as e:
        raise HTTPException(status_code=500, detail=f"Google Search API Error: {str(e)}")

    items = response.json().get("items", [])
    if not items:
        return "No relevant information found."

    # Fetch multiple search results instead of just one
    detailed_response = ""
    for item in items[:3]:  # Increase for longer responses
        snippet = item.get("snippet", "No additional details.")
        title = item.get("title", "Untitled")
        link = item.get("link", "No link")
        detailed_response += f"🔹 **{title}**\n{snippet}\n🔗 [More Info]({link})\n\n"

    return detailed_response

@app.post("/chatbot")
async def chatbot(request: ChatbotRequest):
    if not request.query.strip():
        raise HTTPException(status_code=400, detail="Query cannot be empty.")
    return {"answer": await google_search(request.query)}

# ✅ Root Endpoint to Confirm API Is Running
@app.get("/")
def read_root():
    return {"message": "Chatbot API is live!"}

# ✅ Run Locally (For Development)
if __name__ == "__main__":
    import uvicorn
    uvicorn.run(app, host="0.0.0.0", port=8000)