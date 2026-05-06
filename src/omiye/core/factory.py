from omiye.config import Config
from omiye.core.extractor import OllamaExtractor, AirLLMExtractor, MockExtractor, BaseExtractor

def get_extractor() -> BaseExtractor:
    """Factory to return the configured extractor backend."""
    etype = Config.EXTRACTOR_TYPE.lower()
    
    if etype == "ollama":
        return OllamaExtractor()
    elif etype == "airllm":
        return AirLLMExtractor()
    elif etype == "mock":
        return MockExtractor()
    else:
        raise ValueError(f"Unknown EXTRACTOR_TYPE: {etype}")
