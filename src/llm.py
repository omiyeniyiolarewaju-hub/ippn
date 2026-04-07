import requests
import json
import base64

class LLMExtractor:
    def __init__(self, ollama_url="http://localhost:11434/api/generate", model="qwen2.5-vl"):
        self.url = ollama_url
        self.model = model

    def encode_image(self, image_path):
        """Encode image to base64 string."""
        with open(image_path, "rb") as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def extract_structured_data(self, narrative=None, image_path=None):
        """Send raw text or image to LLM and return structured JSON."""
        prompt = """
        You are an AI police assistant. Extract structured crime data from the provided content.
        Return a valid JSON object with the following fields:
        crime_type, date, time, location, complainant, suspects, weapons, victims, items_stolen, summary.
        """
        
        payload = {
            "model": self.model,
            "prompt": prompt,
            "stream": False,
            "format": "json"
        }

        if image_path:
            payload["prompt"] += "\n\nExtract information directly from the provided image of a handwritten record."
            payload["images"] = [self.encode_image(image_path)]
        elif narrative:
            payload["prompt"] += f"\n\nNarrative Text:\n{narrative}"
        else:
            return {"error": "No data provided for extraction."}

        try:
            response = requests.post(self.url, json=payload)
            response.raise_for_status()
            raw_response = response.json().get("response", "{}")
            return json.loads(raw_response)
        except Exception as e:
            print(f"Error extracting data with LLM: {e}")
            return {"error": str(e)}
