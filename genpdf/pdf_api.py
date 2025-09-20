from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any, List, Optional
import datetime
import json

# Create router for PDF generation APIs
router = APIRouter(prefix="/genpdf", tags=["PDF Generation"])

# Global storage for CV data (in production, use a database)
cv_storage = {}

# Pydantic models for CV data structure
class PersonalInformation(BaseModel):
    name: Optional[str] = None
    email: Optional[str] = None
    phone: Optional[str] = None
    address: Optional[str] = None
    linkedin: Optional[str] = None
    github: Optional[str] = None
    website: Optional[str] = None

class Education(BaseModel):
    degree: Optional[str] = None
    institution: Optional[str] = None
    graduation_year: Optional[str] = None
    gpa: Optional[str] = None

class WorkExperience(BaseModel):
    position: Optional[str] = None
    company: Optional[str] = None
    duration: Optional[str] = None
    responsibilities: Optional[List[str]] = None

class Project(BaseModel):
    name: Optional[str] = None
    description: Optional[str] = None
    technologies: Optional[List[str]] = None
    link: Optional[str] = None

class CVData(BaseModel):
    personal_information: Optional[PersonalInformation] = None
    professional_summary: Optional[str] = None
    education: Optional[List[Education]] = None
    work_experience: Optional[List[WorkExperience]] = None
    skills: Optional[List[str]] = None
    projects: Optional[List[Project]] = None
    certifications: Optional[List[str]] = None
    publications: Optional[List[str]] = None
    awards: Optional[List[str]] = None
    languages: Optional[List[str]] = None
    volunteer: Optional[List[str]] = None
    conferences: Optional[List[str]] = None
    memberships: Optional[List[str]] = None
    references: Optional[List[str]] = None

class ProcessCVRequest(BaseModel):
    cv_data: str  # JSON string from Gemini response

# Pydantic models for request/response
class HelloRequest(BaseModel):
    name: str = "World"
    message: str = ""

class HelloResponse(BaseModel):
    greeting: str
    timestamp: str
    status: str

class PDFRequest(BaseModel):
    title: str
    content: str
    author: str = "Unknown"

# CV Processing endpoints
@router.post("/process-cv")
def process_cv_data(request: ProcessCVRequest):
    """
    Process and store CV data from Gemini response
    """
    try:
        # Parse the JSON string from Gemini
        cv_json = json.loads(request.cv_data)
        
        # Store the data globally (use session_id in production)
        session_id = "default"  # In production, generate unique session IDs
        cv_storage[session_id] = cv_json
        
        return {
            "message": "CV data processed and stored successfully",
            "session_id": session_id,
            "fields_available": list(cv_json.keys()),
            "timestamp": datetime.datetime.now().isoformat()
        }
    except json.JSONDecodeError as e:
        raise HTTPException(status_code=400, detail=f"Invalid JSON format: {str(e)}")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Processing error: {str(e)}")

# Individual CV field endpoints
@router.get("/personal-information")
def get_personal_information(session_id: str = "default"):
    """Get personal information from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "personal_information",
        "data": cv_storage[session_id].get("personal_information", {}),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/professional-summary")
def get_professional_summary(session_id: str = "default"):
    """Get professional summary from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "professional_summary",
        "data": cv_storage[session_id].get("professional_summary", ""),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/education")
def get_education(session_id: str = "default"):
    """Get education information from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "education",
        "data": cv_storage[session_id].get("education", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/work-experience")
def get_work_experience(session_id: str = "default"):
    """Get work experience from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "work_experience",
        "data": cv_storage[session_id].get("work_experience", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/skills")
def get_skills(session_id: str = "default"):
    """Get skills from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "skills",
        "data": cv_storage[session_id].get("skills", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/projects")
def get_projects(session_id: str = "default"):
    """Get projects from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "projects",
        "data": cv_storage[session_id].get("projects", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/certifications")
def get_certifications(session_id: str = "default"):
    """Get certifications from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "certifications",
        "data": cv_storage[session_id].get("certifications", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/publications")
def get_publications(session_id: str = "default"):
    """Get publications from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "publications",
        "data": cv_storage[session_id].get("publications", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/awards")
def get_awards(session_id: str = "default"):
    """Get awards from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "awards",
        "data": cv_storage[session_id].get("awards", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/languages")
def get_languages(session_id: str = "default"):
    """Get languages from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "languages",
        "data": cv_storage[session_id].get("languages", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/volunteer")
def get_volunteer(session_id: str = "default"):
    """Get volunteer experience from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "volunteer",
        "data": cv_storage[session_id].get("volunteer", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/conferences")
def get_conferences(session_id: str = "default"):
    """Get conferences from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "conferences",
        "data": cv_storage[session_id].get("conferences", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/memberships")
def get_memberships(session_id: str = "default"):
    """Get memberships from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "memberships",
        "data": cv_storage[session_id].get("memberships", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/references")
def get_references(session_id: str = "default"):
    """Get references from stored CV data"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "field": "references",
        "data": cv_storage[session_id].get("references", []),
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/all-fields")
def get_all_cv_fields(session_id: str = "default"):
    """Get all CV fields at once"""
    if session_id not in cv_storage:
        raise HTTPException(status_code=404, detail="CV data not found. Please process CV data first.")
    
    return {
        "session_id": session_id,
        "cv_data": cv_storage[session_id],
        "timestamp": datetime.datetime.now().isoformat()
    }

@router.get("/")
def genpdf_home():
    """
    Home endpoint for PDF generation service
    """
    return {
        "message": "Welcome to PDF Generation API",
        "version": "1.0.0",
        "available_endpoints": [
            "/genpdf/process-cv",
            "/genpdf/personal-information",
            "/genpdf/professional-summary", 
            "/genpdf/education",
            "/genpdf/work-experience",
            "/genpdf/skills",
            "/genpdf/projects",
            "/genpdf/certifications",
            "/genpdf/publications",
            "/genpdf/awards",
            "/genpdf/languages",
            "/genpdf/volunteer",
            "/genpdf/conferences",
            "/genpdf/memberships",
            "/genpdf/references",
            "/genpdf/all-fields"
        ]
    }
