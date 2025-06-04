from PyQt5.QtWidgets import QPushButton

class CircularButton(QPushButton):
    
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setStyleSheet(f"""
            QPushButton {{
                border-radius: {(min(self.width(), self.height())) // 0.5}px;
                background-color: #000000;
                color: white;
                font-weight: bold;
            }}
        """)
        self.setFixedSize(70, 70)
    
    def resizeEvent(self, a0):
        side = min(a0.size().width(), a0.size().height())
        self.setFixedSize(side, side)
        super().resizeEvent(a0)