import pytest
import os
import sys

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from omiye.core.factory import get_extractor
from omiye.core.extractor import MockExtractor, OllamaExtractor
from omiye.config import Config

def test_factory_mock():
    """Verify factory returns MockExtractor when configured."""
    Config.EXTRACTOR_TYPE = "mock"
    extractor = get_extractor()
    assert isinstance(extractor, MockExtractor)

def test_factory_ollama():
    """Verify factory returns OllamaExtractor when configured."""
    Config.EXTRACTOR_TYPE = "ollama"
    extractor = get_extractor()
    assert isinstance(extractor, OllamaExtractor)

def test_mock_extraction():
    """Verify the mock extractor returns a valid CrimeReport."""
    extractor = MockExtractor()
    report = extractor.extract("dummy_path.jpg")
    assert report.crime_type == "Mock Crime"
    assert report.summary == "This is a mock result."

def test_config_loading():
    """Verify environment variables are loaded."""
    assert hasattr(Config, "VLM_MODEL")
    assert hasattr(Config, "EXTRACTOR_TYPE")
