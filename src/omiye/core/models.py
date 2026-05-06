from pydantic import BaseModel, Field
from typing import Optional, List

class CrimeReport(BaseModel):
    crime_type: Optional[str] = Field(None, description="Type of crime reported")
    date: Optional[str] = Field(None, description="Date of the incident")
    time: Optional[str] = Field(None, description="Time of the incident")
    location: Optional[str] = Field(None, description="Location of the incident")
    complainant: Optional[str] = Field(None, description="Name of the person filing the report")
    suspects: Optional[List[str]] = Field(default_factory=list, description="Names or descriptions of suspects")
    weapons: Optional[List[str]] = Field(default_factory=list, description="Weapons involved")
    victims: Optional[List[str]] = Field(default_factory=list, description="Names or descriptions of victims")
    items_stolen: Optional[List[str]] = Field(default_factory=list, description="List of items stolen")
    summary: Optional[str] = Field(None, description="Short summary of the incident")
    raw_text: Optional[str] = Field(None, description="Full verbatim text from the document")
