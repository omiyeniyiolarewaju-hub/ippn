from llm import LLMExtractor
from database import DatabaseManager
import os

def process_local_image(image_path):
    if not os.path.exists(image_path):
        print(f"Error: Image not found at {image_path}")
        return

    llm = LLMExtractor()
    db = DatabaseManager()

    print(f"Processing image: {image_path}")

    # Vision Extraction using qwen2.5-vl
    print("\n--- LLM Vision Extraction (qwen2.5-vl) ---\n")
    structured = llm.extract_structured_data(image_path=image_path)
    
    # Extract transcription from structured data
    text = structured.get("transcription", "No transcription available.")
    
    print("\n--- Transcription ---\n")
    print(text)
    
    print("\n--- Structured Data ---\n")
    print(structured)

    # Save to Database
    db.save_report("Local Image Process", text, structured)
    print("\nData saved to database.")

if __name__ == "__main__":
    image_path = "data/better2.jpeg"
    process_local_image(image_path)
