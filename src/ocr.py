import os
import cv2
import easyocr
import numpy as np

class OCRProcessor:
    def __init__(self, languages=['en']):
        self.reader = easyocr.Reader(languages)

    def preprocess_image(self, image_path):
        """Enhance image for better handwritten text recognition."""
        img = cv2.imread(image_path)
        if img is None:
            raise FileNotFoundError(f"Image not found at {image_path}")

        # Convert to grayscale
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        # Noise reduction (Gaussian Blur)
        blurred = cv2.GaussianBlur(gray, (5, 5), 0)

        # Adaptive Binarization (Otsu's Thresholding)
        _, thresh = cv2.threshold(blurred, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)

        return thresh

    def extract_text(self, image_path):
        """Extract text from a handwritten image."""
        processed_img = self.preprocess_image(image_path)
        result = self.reader.readtext(processed_img)
        text = " ".join([res[1] for res in result])
        return text
