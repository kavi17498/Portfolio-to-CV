from fastapi import APIRouter, HTTPException
from pydantic import BaseModel
from typing import Dict, Any
import datetime

# Create router for PDF generation APIs
router = APIRouter(prefix="/genpdf", tags=["PDF Generation"])

# Pydantic models for request/response
class HelloRequest(BaseModel):
    name: str = "World"
    message: str = ""
