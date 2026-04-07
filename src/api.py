import os
from fastapi import FastAPI, UploadFile, File, Form
from src.llm import LLMExtractor
from src.database import DatabaseManager

class OmiyeAPI:
    def __init__(self):
        self.app = FastAPI(title="Omiye Master Vision Extraction API")
        self.llm = LLMExtractor()
        self.db = DatabaseManager()
        self.setup_routes()

    def setup_routes(self):
        @self.app.post("/upload-image/")
        async def upload_image(file: UploadFile = File(...)):
            data_dir = "data"
            os.makedirs(data_dir, exist_ok=True)
            file_path = os.path.join(data_dir, file.filename)

            with open(file_path, "wb") as f:
                f.write(await file.read())

            # Vision Extraction (using qwen2.5-vl)
            structured = self.llm.extract_structured_data(image_path=file_path)
            text = structured.get("transcription", "No transcription available.")

            # Save
            self.db.save_report("Vision Process", text, structured)

            return {
                "message": "Processed successfully using qwen2.5-vl",
                "transcription": text,
                "structured_output": structured
            }

        @self.app.post("/submit-text/")
        async def submit_text(narrative: str = Form(...)):
            structured = self.llm.extract_structured_data(narrative)

            self.db.save_report("Officer Entry", narrative, structured)

            return {
                "message": "Processed successfully",
                "structured_output": structured
            }

# Instantiating the app to be imported by uvicorn
omiye_api = OmiyeAPI()
app = omiye_api.app
