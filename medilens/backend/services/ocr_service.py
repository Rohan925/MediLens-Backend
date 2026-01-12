import pytesseract
import cv2
import os


def extract_text_from_image(image_path: str) -> str:
    """
    Extract text from an image using Tesseract OCR.
    """

    if not os.path.exists(image_path):
        return ""

    # Read image using OpenCV
    image = cv2.imread(image_path)

    if image is None:
        return ""

    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # Improve contrast using thresholding
    gray = cv2.threshold(
        gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU
    )[1]

    # OCR
    text = pytesseract.image_to_string(gray)

    return text.strip()
