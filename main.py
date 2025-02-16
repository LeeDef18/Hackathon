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

        # height, width, _ = img.shape
        # myconfig = r'--psm 11 --oem 3 -l rus'

        # boxes = pytesseract.image_to_boxes(img, config=myconfig)
        # for box in boxes.splitlines():
        #     box = box.split(' ')
        #     img = cv2.rectangle(img, (int(box[1]), height- int(box[2])), (int(box[3]), height- int(box[4])), (0,255,0),2)

        # cv2.imshow('img',img)
        # cv2.waitKey(0)
        # blur = cv2.GaussianBlur(img, (5,5), 0)

        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        result = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
        text = pytesseract.image_to_string(result, lang='rus_ftuned2')

        text = re.sub(r'[^а-яА-Я0-9\s.,!?;-]', '', text)
        
        return text
    except Exception as e:
        print(f"Ошибка при обработке изображения: {e}")
        return None

# image_path = r"tesseract\testfile.png" 
# recognized_text = ocr_image(image_path)
# print(recognized_text)

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