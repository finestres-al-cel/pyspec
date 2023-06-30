
from PyQt6.QtWidgets import QPushButton

class QPushButtonIndex(QPushButton):
    """

    """
    def __init__(self, text, index):
        super().__init__(text)
        self.index = index
