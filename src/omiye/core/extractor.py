import requests
import json
import base64
import os
from abc import ABC, abstractmethod
from omiye.config import Config
from omiye.core.models import CrimeReport

class BaseExtractor(ABC):
    @abstractmethod
    def extract(self, image_path: str) -> CrimeReport:
        pass

    @abstractmethod
    def extract_from_text(self, text: str) -> CrimeReport:
        pass

class OllamaExtractor(BaseExtractor):
    def __init__(self, url=Config.OLLAMA_URL, model=Config.VLM_MODEL):
        self.url = url
        self.model = model
        self.system_prompt = (
            "You are an expert police records assistant. "
            "Analyze the input and extract structured data. "
            "Return ONLY a valid JSON object matching this schema: "
            "{'crime_type': string, 'date': string, 'time': string, 'location': string, "
            "'complainant': string, 'suspects': list, 'weapons': list, 'victims': list, "
            "'items_stolen': list, 'summary': string, 'raw_text': string}. "
            "If a field is missing, set it to null or an empty list for lists."
        )

    def _encode_image(self, image_path: str) -> str:
        with open(image_path, "rb") as f:
            return base64.b64encode(f.read()).decode("utf-8")

    def extract(self, image_path: str) -> CrimeReport:
        payload = {
            "model": self.model,
            "stream": False,
            "format": "json",
            "prompt": self.system_prompt + "\nExtract data from this image.",
            "images": [self._encode_image(image_path)],
        }
        return self._post_request(payload)

    def extract_from_text(self, text: str) -> CrimeReport:
        payload = {
            "model": self.model,
            "stream": False,
            "format": "json",
            "prompt": self.system_prompt + f"\nExtract data from this text: {text}",
        }
        return self._post_request(payload)

    def _post_request(self, payload: dict) -> CrimeReport:
        try:
            response = requests.post(self.url, json=payload, timeout=180)
            response.raise_for_status()
            raw_response = response.json().get("response", "{}")
            data = json.loads(raw_response)
            return CrimeReport(**data)
        except Exception as e:
            return CrimeReport(raw_text=f"Ollama Error: {str(e)}")

class AirLLMExtractor(BaseExtractor):
    def __init__(self, model_path=Config.VLM_MODEL):
        # Lazy import to avoid crashing if airllm isn't installed
        from airllm import AutoModel
        self.model = AutoModel.from_pretrained(
            model_path, 
            profiling_mode=False,
            # AirLLM specific optimization for small VRAM
            compression="4bit" 
        )

    def extract(self, image_path: str) -> CrimeReport:
        # Implementation for VLM image processing with AirLLM
        # Note: AirLLM is primarily for LLMs, VLM support depends on the specific model architecture
        return CrimeReport(raw_text="AirLLM VLM extraction not yet fully implemented.")

    def extract_from_text(self, text: str) -> CrimeReport:
        prompt = f"Extract crime report data from this text as JSON: {text}"
        output = self.model.generate(prompt, max_new_tokens=500)
        # Parse output and return CrimeReport
        return CrimeReport(raw_text=output)

class MockExtractor(BaseExtractor):
    def extract(self, image_path: str) -> CrimeReport:
        return CrimeReport(crime_type="Mock Crime", summary="This is a mock result.")

    def extract_from_text(self, text: str) -> CrimeReport:
        return CrimeReport(crime_type="Mock Text Crime", raw_text=text)
