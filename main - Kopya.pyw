# File: main.py
import os
import random
import sys
from PySide6.QtUiTools import QUiLoader
from PySide6.QtWidgets import QApplication, QDialog
from PySide6.QtCore import QFile, QIODevice
from PyQt6.QtWidgets import QApplication, QMainWindow, QSystemTrayIcon, QMessageBox
from PyQt6.QtGui import QIcon
from PyQt6.QtCore import Qt
from PyQt6 import QtCore
from notification import *

soru_cevap = {}
suanki_soru = ""
suanki_cevap = ""
ilk_uzunluk = 0

def alert_sound():
    import winsound
    winsound.MessageBeep()

def durdur():
    # set window.calisilacak_text text color to red
    window.calisilacak_text.setStyleSheet("color: black;")
    window.calismayaBaslaButton.setText("Çalışmaya başla")
    window.soruinfoLabel.setText(f"Soru:")
    
def calismaya_basla():
    print("Çalışmaya başlanıyor")
    btnTxt = window.calismayaBaslaButton.text()
    
    def baslat():
        global soru_cevap, ilk_uzunluk
        
        text = window.calisilacak_text.toPlainText()
        
        lines = text.split("\n")
        
        soru_cevap = {}
        for line in lines:
            if "<>" in line:
                soru_cevap[line.split("<>")[1].strip()] = line.split("<>")[0].strip()
                soru_cevap[line.split("<>")[0].strip()] = line.split("<>")[1].strip()
            elif ">>" in line:
                soru_cevap[line.split(">>")[0].strip()] = line.split(">>")[1].strip()
            elif "<<" in line:
                soru_cevap[line.split("<<")[1].strip()] = line.split("<<")[0].strip()
        
        ilk_uzunluk = len(soru_cevap)
        print(soru_cevap)
        
        if soru_cevap == {}:
            alert_sound()
            message = "Lütfen en az bir adet flashcard hazırlayınız!"
            width = 400
            height = 50
            notification = NotificationWidget(message, width, height)
            notification.show()
            return
        
        # set window.calisilacak_text text color to white
        window.calisilacak_text.setStyleSheet("color: white;")
        window.calismayaBaslaButton.setText("Çalışmayı durdur")
        window.soruLabel.setText("")
        
        get_next_card()
        
        
     
    
    if "başla" in btnTxt:
        baslat()
    else:
        durdur()

def cevabi_goster():
    window.soruLabel.setText(suanki_soru + "<hr>" + suanki_cevap)

def learned_card():
    global soru_cevap
    soru_cevap.pop(suanki_soru)
    if len(soru_cevap) == 0:
        window.soruLabel.setText("Tebrikler! Tüm flashcard'ları öğrendiniz!")
        message = "Tebrikler! Tüm flashcard'ları öğrendiniz!"
        width = 400
        height = 50
        notification = NotificationWidget(message, width, height)
        notification.show()
        durdur()
        return
    get_next_card()
    window.cevapYaz_text.setText("")
    
def repeat_card():
    if len(soru_cevap) == 1:
        alert_sound()
        message = "Bu şu andaki son flashcard!"
        width = 400
        height = 50
        notification = NotificationWidget(message, width, height)   
        notification.show()
        return
    onceki_soru = suanki_soru
    while onceki_soru == window.soruLabel.text().split("<hr>")[0]:
        get_next_card()
    window.cevapYaz_text.setText("")

def get_next_card():
    global suanki_soru, suanki_cevap
    
    # choose a random question
    suanki_soru = random.choice(list(soru_cevap.keys()))
    suanki_cevap = soru_cevap[suanki_soru]
    #print(suanki_soru, suanki_cevap)
    
    window.soruLabel.setText(suanki_soru)
    window.soruinfoLabel.setText(f"Soru: {len(soru_cevap)}/{ilk_uzunluk}")

def typing_answer():
    global suanki_cevap
    get_answer = window.cevapYaz_text.toPlainText()
    
    if get_answer.lower() == suanki_cevap.lower():
        learned_card()
        window.cevapYaz_text.setText("")

def dosya_sec():
    if window.comboBox.currentText() == "":
        window.calisilacak_text.setText("")
        return
        
    try:
        with open("kartlar/" + window.comboBox.currentText(), "r", encoding="utf-8") as f:
            window.calisilacak_text.setText(f.read())
    except:
        alert_sound()
        message = "Dosyaya erişilemiyor!"
        width = 400
        height = 50
        notification = NotificationWidget(message, width, height)   
        notification.show()

def reload_combo():
    window.comboBox.clear()
    window.comboBox.addItem("")
    for file in os.listdir("kartlar"):
        window.comboBox.addItem(file)

if __name__ == "__main__":
    app = QApplication(sys.argv)

    ui_file_name = "untitled.ui"
    ui_file = QFile(ui_file_name)
    if not ui_file.open(QIODevice.ReadOnly):
        print(f"Cannot open {ui_file_name}: {ui_file.errorString()}")
        sys.exit(-1)
    loader = QUiLoader()
    window = loader.load(ui_file)
    ui_file.close()
    if not window:
        print(loader.errorString())
        sys.exit(-1)

    window.calismayaBaslaButton.clicked.connect(calismaya_basla)
    window.cevabiGosterButton.clicked.connect(cevabi_goster)
    window.ogrendimButton.clicked.connect(learned_card)
    window.tekrarlaButton.clicked.connect(repeat_card)
    
    reload_combo()
    # when type
    window.cevapYaz_text.textChanged.connect(typing_answer)
    
    
    #window.comboBox.currentTextChanged.connect(dosya_sec)
    window.comboBox.currentIndexChanged.connect(dosya_sec)
    window.show()

    sys.exit(app.exec())