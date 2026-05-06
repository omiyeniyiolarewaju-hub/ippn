import sys
import os
import json
import requests

# Add src to path
sys.path.append(os.path.join(os.path.dirname(__file__), "..", "src"))

from omiye.core.extractor import OllamaExtractor
from omiye.core.models import CrimeReport

def check_model_exists(model_name):
    try:
        response = requests.get("http://localhost:11434/api/tags")
        if response.status_code == 200:
            models = [m['name'] for m in response.json().get('models', [])]
            return model_name in models or f"{model_name}:latest" in models
    except:
        return False
    return False

def compare(image_path, model_names):
    results = {}
    for name in model_names:
        if not check_model_exists(name):
            print(f"Skipping {name}: Model not found in Ollama. Run 'ollama pull {name}' first.")
            results[name] = {"error": "Model not found"}
            continue
            
        print(f"Running extraction with {name}...")
        try:
            extractor = OllamaExtractor(model=name)
            report = extractor.extract(image_path)
            results[name] = report.dict()
        except Exception as e:
            results[name] = {"error": str(e)}
    
    output_file = "outputs/comparison_results.json"
    with open(output_file, "w") as f:
        json.dump(results, f, indent=4)
    
    print(f"\n--- Comparison Complete ---")
    print(f"Results saved to {output_file}")
    
    # Simple console summary
    for name, data in results.items():
        if "error" not in data:
            print(f"\n[{name}] Summary: {data.get('summary')}")
        else:
            print(f"\n[{name}] Failed: {data['error']}")

if __name__ == "__main__":
    # Recommended small VLMs for 4GB VRAM
    vlm_candidates = ["qwen2-vl:2b", "moondream"]
    
    sample_image = "data/better2.jpeg"
    if os.path.exists(sample_image):
        compare(sample_image, vlm_candidates)
    else:
        print(f"Sample image not found: {sample_image}")
