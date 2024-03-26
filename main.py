import pytesseract # optical character recognition (OCR)
import cv2 as cv
import pykakasi # 
from translate import Translator
from pynput import mouse
import pyscreenshot as ss

coordinates = list()
def on_click(x, y, button, pressed):
    if pressed:
        coordinates.append((x, y))
    else:
        coordinates.append((x, y))
        return False 
        # it takes coordinates only one time
    
def screenshoter():
    with mouse.Listener(on_click=on_click) as listener:
        listener.join()
    
    pic = ss.grab(bbox=(min(coordinates[0][0],coordinates[1][0]), 
                        min(coordinates[0][1],coordinates[1][1]),
                        max(coordinates[0][0],coordinates[1][0]), 
                        max(coordinates[0][1],coordinates[1][1])))
    pic.save("ss.png")
    return "ss.png"


def translator_TR(text):
    translator = Translator(from_lang="ja", to_lang="tr")
    translation = translator.translate(f"{text}")
    return translation
def translator_EN(text):
    translator = Translator(from_lang="ja", to_lang="en")
    translation = translator.translate(f"{text}")
    return translation


def pull_text(name, choice):
    # Read the image
    img = cv.imread(name)

    # Convert the image to grayscale
    # Perform thresholding
    gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
    ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)
    
    # Apply image-to-string conversion
    if(choice == 1): 
        text = pytesseract.image_to_string(thresh, lang='jpn', config='--tessdata-dir "./data/"')
    if(choice == 2): 
        text = pytesseract.image_to_string(thresh, lang='jpn_vert', config='--tessdata-dir "./data/"')

    # Display the result image
    cv.imshow('Result', thresh)
    # text without ' ' 
    return ''.join(text.split()) 


def furigana(text):
    kks = pykakasi.kakasi()
    text = text
    result = kks.convert(text)
    for item in result:
        print("{}[{}] -> {}".format(
            item['orig'], 
            item['hepburn'].capitalize(), 
            translator_TR(item['orig'])))
    
    print()
    print(f"all sentence (JPN): {text}")
    print(f"all sentence (ENG): {translator_EN(text)}")
    print(f"all sentence (TUR): {translator_TR(text)}")


text = pull_text(screenshoter(), 2)
furigana(text)


cv.waitKey(0)
