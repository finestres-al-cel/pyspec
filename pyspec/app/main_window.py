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
from pyspec.app.load_actions import (
    loadFileMenuActions,
    loadSpectralExtractionActions,
    loadOtherActions
)
from pyspec.app.rotate_image_dialog import RotateImageDialog
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

        self.extractSpectrumActions = loadSpectralExtractionActions(self)
        self.fileActions = loadFileMenuActions(self)
        self.otherActions = loadOtherActions(self)

        self._createToolBar()
        self._createStatusBar()
        self._createMenuBar()

        self.image = None

    def _createToolBar(self):
        """Create tool bars"""
        fileToolBar = QToolBar("File toolbar")
        fileToolBar.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        for menuAction in self.fileActions:
            fileToolBar.addAction(menuAction)
            fileToolBar.addSeparator()
        self.addToolBar(fileToolBar)

        extractSpectrumToolBar = QToolBar("Extract Spectrum toolbar")
        extractSpectrumToolBar.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        for menuAction in self.extractSpectrumActions:
            extractSpectrumToolBar.addAction(menuAction)
            extractSpectrumToolBar.addSeparator()
        self.addToolBar(extractSpectrumToolBar)

        otherToolBar = QToolBar("Other toolbar")
        otherToolBar.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        for menuAction in self.otherActions:
            otherToolBar.addAction(menuAction)
            otherToolBar.addSeparator()
        self.addToolBar(otherToolBar)

    def _createMenuBar(self):
        """Create menu bars"""
        menu = self.menuBar()

        fileMenu = menu.addMenu("&File")
        for menuAction in self.fileActions:
            fileMenu.addAction(menuAction)
            fileMenu.addSeparator()

        extractSpectrumMenu = menu.addMenu("&Extract Spectrum")
        for menuAction in self.extractSpectrumActions:
            extractSpectrumMenu.addAction(menuAction)
            extractSpectrumMenu.addSeparator()

        otherMenu = menu.addMenu("&Other")
        for menuAction in self.otherActions:
            otherMenu.addAction(menuAction)
            otherMenu.addSeparator()

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
            # load image
            self.image = Image(filename)

            # plot image
            self.graphWidget = pg.ImageView()
            self.graphWidget.show()
            self.graphWidget.setImage(self.image.data)
            self.setCentralWidget(self.graphWidget)

            # enable extract spectrum options
            for action in self.extractSpectrumActions:
                action.setEnabled(True)

        except ImageError as error:
            self.statusBar().showMessage(str(error))

    def rotate_image(self):
        """ Rotate image.

        Asks the user for the rotation angle and stores the result
        Then, rotate the image and update the plot
        """

        rotateImgageDialog = RotateImageDialog()
        if rotateImgageDialog.exec():
            try:
                self.image.rotate(rotateImgageDialog.rotateAngleQuestion.text())
            except ImageError as error:
                self.statusBar().showMessage(str(error))
            self.graphWidget.setImage(self.image.data)
