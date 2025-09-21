from fastapi import FastAPI, HTTPException
from fastapi.responses import StreamingResponse
from fastapi.middleware.cors import CORSMiddleware
import requests
import os
from pydantic import BaseModel
from google import genai
from dotenv import load_dotenv
import uvicorn
import json
from pdf_generator import generatepdf

# Pydantic model for CV data input
class CVDataRequest(BaseModel):
    cv_data: dict
    filename: str = None

# Import the PDF generation router
try:
    from genpdf.pdf_api import router as pdf_router
except ImportError:
    pdf_router = None

# Load environment variables
load_dotenv()
GEMINI_API_KEY = os.getenv("GEMINI_API_KEY")

if not GEMINI_API_KEY:
    raise ValueError("GEMINI_API_KEY environment variable not set")

# ✅ Correct client initialization
client = genai.Client(api_key=GEMINI_API_KEY)

app = FastAPI()

# Add CORS middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=["http://localhost:3000"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include the PDF generation router
if pdf_router:
    app.include_router(pdf_router)

baseURL = "https://r.jina.ai/"

@app.post("/generate-pdf")
def generate_pdf_from_data(request: CVDataRequest):
    """
    Generate PDF from provided CV data
    
    Args:
        request: CVDataRequest containing cv_data and optional filename
        
    Returns:
        StreamingResponse: PDF file as downloadable attachment
    """
    try:
        cv_data = request.cv_data
        
        # Generate PDF
        pdf_buffer = generatepdf(cv_data)
        
        # Determine filename
        if request.filename:
            filename = request.filename if request.filename.endswith('.pdf') else f"{request.filename}.pdf"
        else:
            name = cv_data.get('personal_information', {}).get('name', 'CV')
            filename = f"{name.replace(' ', '_')}_CV.pdf"
        
        return StreamingResponse(
            iter([pdf_buffer.read()]),
            media_type='application/pdf',
            headers={"Content-Disposition": f"attachment; filename={filename}"}
        )
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"PDF generation failed: {str(e)}")

@app.get("/scrape/{url:path}")
def getwebcontent(url: str, format: str = "json"):
    full_url = baseURL + url
    try:
        response = requests.get(full_url)
        response.raise_for_status()
        
        resp = client.models.generate_content(
            model="gemini-1.5-flash",
            contents=f"""
            Extract and summarize the following website content into a structured JSON CV with these fields:
            - personal_information (object with name, email, phone, address, linkedin, github, website)
            - professional_summary (string)
            - education (array of objects with degree, institution, graduation_year, gpa)
            - work_experience (array of objects with position, company, duration, responsibilities)
            - skills (array of strings)
            - projects (array of objects with name, description, technologies, link)
            - certifications (array of strings)
            - publications (array of strings)
            - awards (array of strings)
            - languages (array of strings)
            - volunteer (array of strings)
            - conferences (array of strings)
            - memberships (array of strings)
            - references (array of strings)

            Return only valid JSON, no extra text or markdown formatting.
            Content: {response.text}
            """
        )
        
        # Parse and store the CV data
        try:
            # Clean the response text by removing markdown code blocks
            clean_json = resp.text.strip()
            
            # Remove markdown code block markers if present
            if clean_json.startswith('```json'):
                clean_json = clean_json[7:]  # Remove ```json
            if clean_json.startswith('```'):
                clean_json = clean_json[3:]   # Remove ```
            if clean_json.endswith('```'):
                clean_json = clean_json[:-3]  # Remove trailing ```
            
            clean_json = clean_json.strip()
            
            cv_data = json.loads(clean_json)
            
            # Store in global variable for individual access
            session_id = "default"
            try:
                from genpdf.pdf_api import cv_storage
                cv_storage[session_id] = cv_data
            except ImportError:
                pass  # pdf_api not available, skip storage
            
            # Return PDF if format=pdf, otherwise return JSON
            if format.lower() == "pdf":
                pdf_buffer = generatepdf(cv_data)
                name = cv_data.get('personal_information', {}).get('name', 'CV')
                filename = f"{name.replace(' ', '_')}_CV.pdf"
                return StreamingResponse(
                    iter([pdf_buffer.read()]),
                    media_type='application/pdf',
                    headers={"Content-Disposition": f"attachment; filename={filename}"}
                )
            
            return {
                "message": "CV data extracted and stored successfully",
                "session_id": session_id,
                "raw_content": resp.text,
                "parsed_data": cv_data,
                "parsed_fields": list(cv_data.keys()),
                "access_endpoints": {
                    "personal_information": f"/genpdf/personal-information",
                    "professional_summary": f"/genpdf/professional-summary", 
                    "education": f"/genpdf/education",
                    "work_experience": f"/genpdf/work-experience",
                    "skills": f"/genpdf/skills",
                    "projects": f"/genpdf/projects",
                    "certifications": f"/genpdf/certifications",
                    "publications": f"/genpdf/publications",
                    "awards": f"/genpdf/awards",
                    "languages": f"/genpdf/languages",
                    "volunteer": f"/genpdf/volunteer",
                    "conferences": f"/genpdf/conferences",
                    "memberships": f"/genpdf/memberships",
                    "references": f"/genpdf/references",
                    "all_fields": f"/genpdf/all-fields"
                }
            }
        except json.JSONDecodeError as e:
            # If parsing fails, return raw content with more details
            return {
                "message": "CV data extracted but parsing failed",
                "error": str(e),
                "raw_content": resp.text,
                "note": "Use /genpdf/process-cv endpoint to manually process this data",
                "debug_info": f"Error at character {e.pos if hasattr(e, 'pos') else 'unknown'}"
            }
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


if __name__ == "__main__":
    uvicorn.run("main:app", host="0.0.0.0", port=8000, reload=True)
    