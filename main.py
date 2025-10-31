import pytesseract
import cv2
import re
import os
import csv

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

def ocr_image(image_path):
    try:
        img = cv2.imread(image_path)
        if img is None:
            print(f"Ошибка: Не удалось загрузить изображение {image_path}")
            return None 

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(result, lang='rus_ftuned2')

        text = re.sub(r'[^а-яА-Я0-9\s.,!?;-]', '', text)
        
        return text
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        return None

data_dir = r"E:\hac\asd\tesseract\tessdata\dataset"

for filename in os.listdir(data_dir):
    if filename.endswith(('.png', '.jpg', '.jpeg')):
        filepath = os.path.join(data_dir, filename)
        try:
            recognized_text = ocr_image(filepath)
            print(recognized_text)
        except Exception as e:
            print(f"Ошибка при обработке файла {filename}: {e}")

with open('ouput.csv', 'w', newline='') as file:
    writer = csv.writer(file)

    writer.writerows(recognized_text.split('\n'))
