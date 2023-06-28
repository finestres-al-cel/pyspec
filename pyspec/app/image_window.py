"""pyspec image window"""

from PyQt6 import QtCore
from PyQt6.QtWidgets import QWidget
import pyqtgraph as pg

from pyspec.app.environment import WIDTH, HEIGHT

class ImageWindow(QWidget):
    """
    Image window

    Methods
    -------
    __init__

    Attributes
    ----------

    """
    def __init__(self, image, width=WIDTH, height=HEIGHT):
        super().__init__()

        self.image = image

        self.setWindowTitle(self.image.filename)
        self.setWindowFlags(QtCore.Qt.WindowType.WindowStaysOnTopHint)
        self.resize(width, height)

        self.graphWidget = pg.ImageView()
        self.graphWidget.show()
        self.graphWidget.setImage(self.image.data)
        self.setCentralWidget(self.graphWidget)
