"""pyspec main window"""
import sys
import os

from PyQt6.QtCore import QSize, Qt
from PyQt6.QtGui import QAction, QIcon
from PyQt6.QtWidgets import (
    QApplication,
    QCheckBox,
    QLabel,
    QMainWindow,
    QStatusBar,
    QToolBar,
)

WIDTH = 800
HEIGHT = 800
ICON_SIZE = 30

THIS_DIR = os.path.dirname(os.path.abspath(__file__))
BUTTONS_PATH = f"{THIS_DIR}/button_plots/"

class MainWindow(QMainWindow):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Pyspec")
        self.resize(WIDTH, HEIGHT)

        label = QLabel("Welcome to Pyspec")
        label.setAlignment(Qt.AlignmentFlag.AlignCenter)

        self.setCentralWidget(label)

        self.menuActions = []
        self._loadActions()

        self._createToolBar()
        self._createStatusBar()
        self._createMenuBar()


    def _createToolBar(self):
        toolbar = QToolBar("Pyspec toolbar")
        toolbar.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        self.addToolBar(toolbar)

        for menuAction in self.menuActions:
            toolbar.addAction(menuAction)
            toolbar.addSeparator()

    def _createStatusBar(self):
        self.setStatusBar(QStatusBar(self))

    def _createMenuBar(self):
        menu = self.menuBar()

        file_menu = menu.addMenu("&File")
        for menuAction in self.menuActions:
            file_menu.addAction(menuAction)
            file_menu.addSeparator()

    def _loadActions(self):
        load_spectrum_option = QAction(
            QIcon(f"{BUTTONS_PATH}/load_image.png"),
            "&Load Spectrum",
            self)
        load_spectrum_option.setStatusTip("Load Spectrum")
        load_spectrum_option.triggered.connect(self.onMyToolBarButtonClick)
        load_spectrum_option.setCheckable(True)
        self.menuActions.append(load_spectrum_option)

        extract_spectrum_option = QAction(
            QIcon(f"{BUTTONS_PATH}/extract_spectrum.jpg"),
            "&Extract Spectrum",
            self)
        extract_spectrum_option.setStatusTip("Extract Spectrum")
        extract_spectrum_option.triggered.connect(self.onMyToolBarButtonClick)
        extract_spectrum_option.setCheckable(True)
        self.menuActions.append(extract_spectrum_option)

        plot_raw_spectrum_option = QAction(
            QIcon(f"{BUTTONS_PATH}/plot_spec.png"),
            "&Plot Spectrum",
            self)
        plot_raw_spectrum_option.setStatusTip("Plot Spectrum")
        plot_raw_spectrum_option.triggered.connect(self.onMyToolBarButtonClick)
        plot_raw_spectrum_option.setCheckable(True)
        self.menuActions.append(plot_raw_spectrum_option)

        set_calibration_option = QAction(
            QIcon(f"{BUTTONS_PATH}/set_calib.png"),
            "&Set Calibration",
            self)
        set_calibration_option.setStatusTip("Set Calibration")
        set_calibration_option.triggered.connect(self.onMyToolBarButtonClick)
        set_calibration_option.setCheckable(True)
        self.menuActions.append(set_calibration_option)

        load_calibration_option = QAction(
            QIcon(f"{BUTTONS_PATH}/load_calib.png"),
            "&Load Calibration",
            self)
        load_calibration_option.setStatusTip("Load Calibration")
        load_calibration_option.triggered.connect(self.onMyToolBarButtonClick)
        load_calibration_option.setCheckable(True)
        self.menuActions.append(load_calibration_option)


    def onMyToolBarButtonClick(self, s):
        print("click", s)

if __name__ == "__main__":
    app = QApplication([])
    mainWindow = MainWindow()
    mainWindow.show()
    sys.exit(app.exec())
