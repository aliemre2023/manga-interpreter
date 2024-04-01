import pytesseract # optical character recognition (OCR)
import cv2 as cv
import pykakasi # 
from translate import Translator
from pynput import mouse
import pyscreenshot as ss
import sys
import pyautogui

from PyQt5.QtWidgets import QApplication, QMainWindow, QLabel, QPushButton, QComboBox, QHBoxLayout
from PyQt5.QtGui import QPixmap, QPalette, QColor

from include import translator
from include.lists import language_options

class App(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Manga Interpreter")

        self.screen_width, self.screen_height = pyautogui.size()
        self.mode = True
        self.screenshot = None
        self.coordinates = []
        self.ss_label = QLabel(self)
        self.translate_to = "EN"

        self.select_button = QPushButton(self)
        self.choice = int(1)
        self.choice1_button = QPushButton(self)
        self.choice2_button = QPushButton(self)
        self.convert_button = QPushButton(self)
        self.mode_button = QPushButton(self)

        self.language_to = QLabel(self)
    
        self.initUI()

    def initUI(self):
        self.setGeometry(int((self.screen_width)*8/10), 0, int((self.screen_width)*2/10), int(self.screen_height))
        self.setStyleSheet("background-color: lightyellow;")

        palette1 = QPalette()
        text_color = QColor(25, 33, 255)
        palette1.setColor(QPalette.WindowText, text_color)
        
        self.select_button = QPushButton("Select", self)
        self.select_button.setGeometry(0, 0, 50, 50)
        self.select_button.setStyleSheet("background-color: pink;")
        self.select_button.clicked.connect(self.screenshoter)

        self.choice1_button = QPushButton("H", self)
        self.choice1_button.setGeometry(50, 0, 25, 25)
        self.choice1_button.setStyleSheet("background-color: purple;")
        self.choice1_button.clicked.connect(lambda: self.set_choice(1))
        self.choice2_button = QPushButton("V", self)
        self.choice2_button.setGeometry(50, 25, 25, 25)
        self.choice2_button.setStyleSheet("background-color: purple;")
        self.choice2_button.clicked.connect(lambda: self.set_choice(2))

        self.convert_button = QPushButton("Convert", self)
        self.convert_button.setGeometry(75, 0, 50, 50)
        self.convert_button.setStyleSheet("background-color: lightblue;")
        self.convert_button.clicked.connect(lambda: self.pull_text(self.screenshot, self.choice))

        self.mode_button = QPushButton(".", self)
        self.mode_button.setGeometry(125, 0, 25, 50)
        self.mode_button.setStyleSheet("background-color: gray;")
        self.mode_button.clicked.connect(lambda: self.resizer())

        self.language = QComboBox(self)
        self.language.setGeometry(150, 0, 0, 50)
        self.language.setStyleSheet("background-color: darkgreen;")
        self.language.currentIndexChanged.connect(self.language_preference)
        language_list = language_options.to_list()
        self.language.setEditable(True)
        self.language.addItems(language_list)
        self.language.adjustSize()

        self.language_to = QLabel(self)
        self.language_to.setGeometry(150, 20, 80, 30)
        self.language_to.setStyleSheet("background-color: darkgreen")
        self.language_to.setWordWrap(True)
    
        self.words_text = QLabel(self)
        self.jpn_text = QLabel(self)
        self.lang_text = QLabel(self)

        self.words_text.setGeometry(10, int((self.screen_height)*4/10) + 100, int(int(self.screen_width)*2/10) - 20, int(self.screen_height - 225) - int(((self.screen_height)*4/10) + 100) - 10)
        self.words_text.setWordWrap(True)
        self.words_text.setPalette(palette1)
        
        self.jpn_text.setGeometry(10, self.screen_height - 225, int(int(self.screen_width)*2/10) - 20, 80)
        self.jpn_text.setWordWrap(True)
        self.jpn_text.setPalette(palette1)
        
        self.lang_text.setGeometry(10, self.screen_height - 140, int(int(self.screen_width)*2/10) - 20, 80)
        self.lang_text.setWordWrap(True)
        self.lang_text.setPalette(palette1)

    def language_preference(self):
        self.translate_to = self.language.currentIndex()
        print(self.translate_to)
        self.language_to.setText(language_options.language_names[language_options.language_idx[self.translate_to]])

    def resizer(self):
        if(self.mode):
            self.setGeometry(self.screen_width - 150, 0, 150, 50)
            self.mode_button.setText("...")
            self.mode = False
        else:
            self.setGeometry(int((self.screen_width)*8/10), 0, int((self.screen_width)*2/10), int(self.screen_height))
            self.mode_button.setText(".")
            self.mode = True
    
    def set_choice(self, choice_val):
        self.choice = choice_val
        if choice_val == 1:
            self.choice1_button.setStyleSheet("background-color: green;")
            self.choice2_button.setStyleSheet("background-color: purple;")
        else:
            self.choice2_button.setStyleSheet("background-color: green;")
            self.choice1_button.setStyleSheet("background-color: purple;")

    def on_click(self, x, y, button, pressed):
        if pressed:
            self.coordinates.append((x, y))
        else:
            self.coordinates.append((x, y))
            return False 
        
    def screenshoter(self):
        with mouse.Listener(on_click=self.on_click) as listener:
            listener.join()
        
        pic = ss.grab(bbox=(min(self.coordinates[0][0],self.coordinates[1][0]), 
                            min(self.coordinates[0][1],self.coordinates[1][1]),
                            max(self.coordinates[0][0],self.coordinates[1][0]), 
                            max(self.coordinates[0][1],self.coordinates[1][1])))
        saved_path = "./saved/ss.png"
        pic.save(saved_path)
        self.coordinates.clear()

        ss_path = saved_path
        self.screenshot = saved_path
        pixmap = QPixmap(ss_path)
        image = cv.imread(ss_path)

        desired_width = int((self.screen_width)*2/10) - int((self.screen_width)*1/20)

        ratio = pixmap.height() / pixmap.width()
        desired_height = int(desired_width * ratio)
        if(desired_height > (self.screen_height)*4/10):
            desired_height = int((self.screen_height)*4/10)
            desired_width = int(desired_height / ratio)
        new_size = (desired_width, desired_height)

        resized_image = cv.resize(image, new_size)
        resized_path = "./saved/ss_resized.png"
        cv.imwrite(resized_path, resized_image)
        pixmap = QPixmap(resized_path)

        starting_point = ((self.screen_width)*2/10 - (resized_image.shape[1]))/2
        self.ss_label.setGeometry(round(starting_point), 75, pixmap.width(), pixmap.height())
        self.ss_label.setPixmap(pixmap)

    def pull_text(self, name, choice):
        img = cv.imread(str(name))

        gray = cv.cvtColor(img, cv.COLOR_BGR2GRAY)
        ret, thresh = cv.threshold(gray, 0, 255, cv.THRESH_BINARY_INV + cv.THRESH_OTSU)

        if(choice == 1): 
            text = pytesseract.image_to_string(thresh, lang='jpn', config='--tessdata-dir "./data/"')
        if(choice == 2): 
            text = pytesseract.image_to_string(thresh, lang='jpn_vert', config='--tessdata-dir "./data/"')

        return self.fuginator(''.join(text.split())) 
    
    def fuginator(self, text):
        kks = pykakasi.kakasi()
        text = text
        result = kks.convert(text)
        self.words_text.setStyleSheet("border: 2px solid #aac3ff")
        words = ""
        language = language_options.language_idx[self.translate_to]
        for item in result:   
            translated_word = language_options.func_selecter(language, item['orig'])
            words += "{}[{}] -> {}\n".format(
                item['orig'], 
                item['hepburn'].capitalize(), 
                translated_word,
            )
            
            self.words_text.setText(words)
            
        
        self.jpn_text.setStyleSheet("border: 2px solid #ff33ff")
        text1 = f"(JPN): {text}"
        self.jpn_text.setText(text1)

        self.lang_text.setStyleSheet("border: 2px solid #af33ff")
        translated_text = language_options.func_selecter(language, text)
        text2 = f"({language}): {translated_text}"
        self.lang_text.setText(text2)



if __name__ == "__main__":
    app = QApplication(sys.argv)
    mainWindow = App()
    mainWindow.show()
    sys.exit(app.exec())