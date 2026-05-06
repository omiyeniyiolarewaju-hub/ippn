import cv2
import easyocr
import numpy as np
import os

class OCREngine:
    def __init__(self, languages=['en']):
        self.reader = easyocr.Reader(languages)

    def preprocess(self, image_path: str) -> np.ndarray:
        """Enhance image for better text recognition."""
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image not found at {image_path}")

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)
        return thresh

    def extract_text(self, image_path: str) -> str:
        """Extract text from an image using EasyOCR."""
        processed_img = self.preprocess(image_path)
        result = self.reader.readtext(processed_img)
        text = " ".join([res[1] for res in result])
        return text
