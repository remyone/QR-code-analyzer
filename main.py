import cv2
from qreader import QReader
from urllib.parse import urlparse

def analyze_qr_data(data: str) -> str:
    if not data:
        return "No QR code data found."

    parsed = urlparse(data)

    if parsed.scheme in ("http", "https") and parsed.netloc:
        if parsed.scheme == "http":
            return f"Dangerous: uses insecure HTTP URL -> {data}"
        return f"Safe-looking: HTTPS URL -> {data}"

    if parsed.scheme and parsed.scheme not in ("http", "https"):
        return f"Dangerous: suspicious protocol '{parsed.scheme}' -> {data}"

    return f"Unknown / possibly unsafe: not a normal URL -> {data}"

def scan_qr(image_path: str):
    qreader = QReader()

    image = cv2.imread(image_path)
    if image is None:
        print("Could not open image.")
        return

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    decoded_text = qreader.detect_and_decode(image=image)

    if not decoded_text:
        print("No QR code detected.")
        return

    for i, data in enumerate(decoded_text, start=1):
        if data:
            print(f"QR {i}: {data}")
            print(analyze_qr_data(data))
        else:
            print(f"QR {i}: empty result")

if __name__ == "__main__":
    path = input("Enter image path: ").strip()
    scan_qr(path)
