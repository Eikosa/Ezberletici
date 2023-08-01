import sys
from PyQt6.QtWidgets import QApplication, QWidget, QLabel, QVBoxLayout, QProxyStyle
from PyQt6.QtCore import QTimer, Qt, QPropertyAnimation

class NotificationWidget(QWidget):
    def __init__(self, message, width=300, height=100, timeout=5000):
        super().__init__()

        self.message = message
        self.width = width
        self.height = height

        self.label = QLabel(self.message, self)
        self.label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        layout = QVBoxLayout()
        layout.addWidget(self.label)
        self.setLayout(layout)

        # disable all focus, so the widget cannot be focused
        self.setFocusPolicy(Qt.FocusPolicy.NoFocus)        
        self.setWindowFlags(Qt.WindowType.FramelessWindowHint | Qt.WindowType.WindowStaysOnTopHint)
        self.setAttribute(Qt.WidgetAttribute.WA_TranslucentBackground)
        self.setAttribute(Qt.WidgetAttribute.WA_ShowWithoutActivating)
        #self.setStyleSheet("background-color: rgba(50, 50, 50, 200); color: white; font-size: 16px; padding: 8px;")
        self.setStyleSheet("background-color: rgba(255, 255, 255, 200); color: dark; font-size: 16px; padding: 8px;")

        self.show_animation_duration = 500  # 1 saniye
        self.hide_animation_duration = 1000  # 1 saniye

        self.timer = QTimer(self)
        self.timer.timeout.connect(self.hide_animation)
        self.timer.start(timeout)  # 5000 milisaniye sonra otomatik olarak kaybolacak

        screen_geo = QApplication.primaryScreen().geometry()
        self.setGeometry(screen_geo.width() - self.width - 10, # -10
                         screen_geo.height() - self.height - 20, # -10
                         self.width, 
                         self.height)


    def show_animation(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(self.show_animation_duration)
        self.animation.setStartValue(0.0)
        self.animation.setEndValue(1.0)
        self.animation.start()

    def hide_animation(self):
        self.animation = QPropertyAnimation(self, b"windowOpacity")
        self.animation.setDuration(self.hide_animation_duration)
        self.animation.setStartValue(1.0)
        self.animation.setEndValue(0.0)
        self.animation.finished.connect(self.close)
        self.animation.start()

    def show(self):
        super().show()
        self.show_animation()

if __name__ == "__main__":
    app = QApplication(sys.argv)

    message = "Merhaba, bu bir animasyonlu bildirim kutusu!"
    width = 400
    height = 150
    notification = NotificationWidget(message, width, height)
    notification.show()

    sys.exit(app.exec())
