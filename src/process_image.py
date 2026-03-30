from src.ocr import OCRProcessor
from src.llm import LLMExtractor
from src.database import DatabaseManager
import os

def process_local_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    ocr = OCRProcessor()
    llm = LLMExtractor()
    db = DatabaseManager()

    print(f"Processing image: {image_path}")

    # OCR Extract
    try:
        text = ocr.extract_text(image_path)
        print("\n--- OCR Text ---\n")
        print(text)
    except Exception as e:
        text = f"OCR failed: {str(e)}"
        print(text)

    # Direct Vision Extraction
    print("\n--- LLM Structured Data Extraction ---\n")
    structured = llm.extract_structured_data(image_path=image_path)
    print(structured)

    # Save to Database
    db.save_report("Local Image Process", text, structured)
    print("\nData saved to database.")

if __name__ == "__main__":
    image_path = "data/better2.jpeg"
    process_local_image(image_path)
