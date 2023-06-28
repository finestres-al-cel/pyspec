"""pyspec main window"""
import os

from PyQt6.QtCore import QSize, Qt, pyqtSlot
from PyQt6.QtWidgets import (
    QCheckBox,
    QFileDialog,
    QLabel,
    QMainWindow,
    QPushButton,
    QStatusBar,
    QToolBar,
)
import pyqtgraph as pg

from pyspec.app.environment import WIDTH, HEIGHT, ICON_SIZE
from pyspec.app.image_window import ImageWindow
from pyspec.app.load_actions import loadMainActions
from pyspec.errors import ImageError
from pyspec.image import Image

class MainWindow(QMainWindow):
    """Main Window

    Methods
    -------
    __init__
    _createToolBar
    _createMenuBar
    _createStatusBar
    _loadActions

    Attributes
    ----------
    centralWidget: QtWidget
    Central widget

    image: Image
    Opened image

    menuActions: list of QAction
    List of menu items. They are plotted in the menu and also in the toolbar
    """
    def __init__(self):
        """Initialize class instance """
        super().__init__()

        self.setWindowTitle("Pyspec")
        self.resize(WIDTH, HEIGHT)

        self.centralWidget = QLabel("Welcome to Pyspec")
        self.centralWidget.setAlignment(Qt.AlignmentFlag.AlignCenter)
        self.setCentralWidget(self.centralWidget)

        self.menuActions = loadMainActions(self)

        self._createToolBar()
        self._createStatusBar()
        self._createMenuBar()

        self.image = None

    def _createToolBar(self):
        """Create tool bar """
        toolbar = QToolBar("Pyspec toolbar")
        toolbar.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.addToolBar(toolbar)

        for menuAction in self.menuActions:
            toolbar.addAction(menuAction)
            toolbar.addSeparator()

    def _createMenuBar(self):
        """Create menu bar"""
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        for menuAction in self.menuActions:
            file_menu.addAction(menuAction)
            file_menu.addSeparator()

    def _createStatusBar(self):
        """Create status bar"""
        self.setStatusBar(QStatusBar(self))

    def onMyToolBarButtonClick(self, s):
        print("click", s)

    @pyqtSlot()
    def open_file(self):
        """Open dialog to select and open file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "${HOME}",
            "Fits Files (*fits *.fits *.fits.gz);; All files (*)",
        )

        try:
            self.image = Image(filename)
            self.graphWidget = pg.ImageView()
            self.graphWidget.show()
            self.graphWidget.setImage(self.image.data)
            self.setCentralWidget(self.graphWidget)
            #image = Image(filename)
            #self.imageWindow = ImageWindow(
            #    image, width=0.7*WIDTH, height=0.7*HEIGHT)
            #self.imageWindow.show()
        except ImageError as error:
            self.statusBar().showMessage(str(error))
