"""Extension of QPushButton to store the button index"""
from PyQt6.QtWidgets import QPushButton

class QPushButtonIndex(QPushButton):
    """Extension of QPushButton to store the button index

    Methods
    -------
    __init__

    Attributes
    ----------
    index: int
    The button index
    """
    def __init__(self, text, index):
        """Initialize class instance

        Arguments
        ---------
        test: str
        The text to be shown in the button

        index: int
        The button index
        """
        super().__init__(text)
        self.index = index
