import cv2
import colorama
from colorama import Fore, init
from qreader import QReader
from urllib.parse import urlparse
from qrdet import QRDetector

def analyze_qr_data(data: str) -> str:
    if not data:
        return Fore.RED + "Не получилось найти никаких данных в QR-коде"

    parsed = urlparse(data)

    if parsed.scheme in ("http", "https") and parsed.netloc:
        if parsed.scheme == "http":
            return Fore.RED + f"Опасно: использует незащищенный протокол - HTTP ; URL -> {data}"
        return Fore.GREEN + f"Выглядит безопасно: протокол - HTTPS ; URL -> {data}"

    if parsed.scheme and parsed.scheme not in ("http", "https"):
        return Fore.RED + f"Опасно: подозрительный протокол '{parsed.scheme}' -> {data}"

    return Fore.RED + f"Неизвестный / вероятно небезопасно: необычный URL -> {data}"

def scan_qr(image_path: str):
    init()
    qreader = QReader()

    image = cv2.imread(image_path)
    if image is None:
        print(Fore.RED + "Не смог открыть изображение")
        #print("Could not open image.")
        return

    image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
    decoded_text = qreader.detect_and_decode(image=image)

    if not decoded_text:
        print(Fore.RED + "Не смог распознать QR-код")
        return

    for i, data in enumerate(decoded_text, start=1):
        if data:
            print(f"QR-код {i}: " + Fore.YELLOW + f"{data}")
            print(analyze_qr_data(data))
        else:
            print(Fore.RED + f"QR-код {i}: пустой результат")

if __name__ == "__main__":
    path = input("Введите путь к изображению QR-кода: ").strip()
    scan_qr(path)
    char : str = str(input("Нажмите любую кнопку + enter для выхода из программы: "))