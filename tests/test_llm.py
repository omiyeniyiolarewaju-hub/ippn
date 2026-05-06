import sys
import json
sys.path.insert(0, ".")

from src.llm import LLMExtractor

image_path = "data/better2.jpeg"

llm = LLMExtractor()

print(f"Testing LLM extraction on: {image_path}\n")
result = llm.extract(image_path)

print(json.dumps(result, indent=2))
