import cv2
import pytesseract
from PIL import Image
import os

def read_scanned_inovice(invoice_image):

    # Load image
    img = cv2.imread("example_image.jpg")
    # Convert image to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    # Apply threshold to convert to binary image
    threshold_img = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]
    # Pass the image through pytesseract
    text = pytesseract.image_to_string(threshold_img)
    # Print the extracted text
    print(text)