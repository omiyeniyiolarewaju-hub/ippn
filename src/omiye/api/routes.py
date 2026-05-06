import os
import shutil
from fastapi import APIRouter, UploadFile, File, Form, HTTPException
from omiye.core.factory import get_extractor
from omiye.db.manager import DatabaseManager
from omiye.core.models import CrimeReport

router = APIRouter()
extractor = get_extractor()
db = DatabaseManager()

@router.post("/process-report/", response_model=CrimeReport)
async def process_report(file: UploadFile = File(...)):
    temp_dir = "data/uploads"
    os.makedirs(temp_dir, exist_ok=True)
    file_path = os.path.join(temp_dir, file.filename)

    with open(file_path, "wb") as buffer:
        shutil.copyfileobj(file.file, buffer)

    try:
        report = extractor.extract(file_path)
        db.save_report(report)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

@router.post("/process-text/", response_model=CrimeReport)
async def process_text(text: str = Form(...)):
    # This shows the VLM working as a standard LLM
    try:
        # We can reuse the same extractor logic but without an image
        # In a real scenario, we'd have a text-only prompt
        report = extractor.extract_from_text(text)
        db.save_report(report)
        return report
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
