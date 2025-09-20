from fastapi import FastAPI, HTTPException
import requests
import os
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import uvicorn
import json

# Import the PDF generation router
from genpdf.pdf_api import router as pdf_router

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# ✅ Correct client initialization
client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()

# Include the PDF generation router
app.include_router(pdf_router)

baseURL = "https://r.jina.ai/"

@app.get("/")
def home():
    return {"message": "Hello World"}

@app.get("/scrape/{url:path}")
def getwebcontent(url: str):
    full_url = baseURL + url
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        resp = client.models.generate_content(
        model="gemini-1.5-flash",
        contents=f"""
        Extract and summarize the following website content into a structured JSON CV with these fields:
        - personal_information
        - professional_summary
        - education
        - work_experience
        - skills
        - projects
        - certifications
        - publications
        - awards
        - languages
        - volunteer
        - conferences
        - memberships
        - references

        Return only valid JSON, no extra text.
        Content: {response.text}
        """
    )
        
        
        return {"content": resp.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

class Message(BaseModel):
    text: str

@app.post("/sayhi")
def say_hi(message: Message):
    try:
        resp = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"Say hi to: {message.text}"
        )
        return {"reply": resp.text}
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
