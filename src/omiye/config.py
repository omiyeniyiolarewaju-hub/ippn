import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    # Extractor selection: 'ollama', 'airllm', or 'mock'
    EXTRACTOR_TYPE = os.getenv("EXTRACTOR_TYPE", "ollama")
    
    OLLAMA_URL = os.getenv("OLLAMA_URL", "http://localhost:11434/api/generate")
    # Using Qwen2-VL-2B which is perfect for 4GB VRAM
    VLM_MODEL = os.getenv("VLM_MODEL", "qwen2-vl:2b")
    
    # AirLLM specific
    AIRLLM_CACHE_DIR = os.getenv("AIRLLM_CACHE_DIR", "outputs/airllm_cache")
    
    DATABASE_PATH = os.getenv("DATABASE_PATH", "outputs/omiye.db")
    DEBUG = os.getenv("DEBUG", "True").lower() == "true"
