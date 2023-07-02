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
    QMessageBox,
)

from pyspec.app.environment import WIDTH, HEIGHT, ICON_SIZE
from pyspec.app.error_dialog import ErrorDialog
from pyspec.app.image_view import ImageView
from pyspec.app.load_actions import (
    loadFileMenuActions,
    loadSpectralExtractionActions,
    loadSpectrumActions
)
from pyspec.app.rotate_image_dialog import RotateImageDialog
from pyspec.app.spectrum_view import SpectrumView
from pyspec.app.success_dialog import SuccessDialog
from pyspec.app.utils import getFileType
from pyspec.errors import CalibrationError, ImageError, SpectrumError
from pyspec.calibration import Calibration
from pyspec.image import Image
from pyspec.spectrum import Spectrum


class MainWindow(QMainWindow):
    """Main Window

    Methods
    -------
    (see QMainWindow)
    __init__
    _createToolBar
    _createMenuBar
    _createStatusBar
    _loadActions

    Attributes
    ----------
    (see QMainWindow)

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
        self.spectrumActions = loadSpectrumActions(self)

        self._createToolBar()
        self._createStatusBar()
        self._createMenuBar()

        self.image = None
        self.imageView = None
        self.spectrum = None
        self.spectrumView = None
        self.calibration = None

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

        spectrumToolBar = QToolBar("Spectrum")
        spectrumToolBar.setIconSize(QSize(ICON_SIZE, ICON_SIZE))
        for menuAction in self.spectrumActions:
            spectrumToolBar.addAction(menuAction)
            spectrumToolBar.addSeparator()
        self.addToolBar(spectrumToolBar)

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

        spectrumMenu = menu.addMenu("&Spectrum")
        for menuAction in self.spectrumActions:
            spectrumMenu.addAction(menuAction)
            spectrumMenu.addSeparator()

    def _createStatusBar(self):
        """Create status bar"""
        self.setStatusBar(QStatusBar(self))

    def activateChooseLimitOnClick(self, checked, sender):
        """Activate/deactivate choose limits on click.

        If the sender is now active, then deactivate all other actions in the
        Extract Spectrum menu.


        Arguments
        ---------
        checked: boolean
        True if the sender is now checked. False otherwise.

        sender: QAction
        Qaction starting the function. Must be one of the Extract Spectrum
        menu
        """
        if checked:
            # uncheck the other actions
            for menuAction in self.extractSpectrumActions:
                if (menuAction != sender and menuAction.isCheckable()
                    and menuAction.isChecked()):
                    menuAction.setChecked(False)

            # activate set limit on clicking
            message = self.imageView.activateChooseLimitOnClick(sender)

        else:
            # de activate set limit on clicking
            message = self.imageView.deactivateChooseLimitOnClick()

        self.statusBar().showMessage(message)

    def activateSetCalibration(self, checked, sender):
        """Activate/deactivate set calibration.

        If the sender is now active, then deactivate all other actions in the
        Spectrum menu.

        Arguments
        ---------
        checked: boolean
        True if the sender is now checked. False otherwise.

        sender: QAction
        Qaction starting the function. Must be one of the Extract Spectrum
        menu
        """
        if checked:
            # uncheck the other actions
            for menuAction in self.spectrumActions:
                if (menuAction != sender and menuAction.isCheckable()
                    and menuAction.isChecked()):
                    menuAction.setChecked(False)

            # activate set limit on clicking
            message = self.spectrumView.activateSetCalibrationPoints()

        else:
            # de activate set limit on clicking
            message = self.spectrumView.deactivateSetCalibrationPoints()

        self.statusBar().showMessage(message)

    def calibrate(self):
        """Calibrate spectrum"""
        self.spectrum.wavelength = self.calibration.calibrate(
            self.spectrum.flux.size)

        print(self.spectrum.wavelength)
        self.spectrumView.setSpectrum(self.spectrum)

        successDialog = SuccessDialog("Calibration success")
        successDialog.exec()

    @pyqtSlot()
    def extractSpectrum(self):
        """Extract the spectrum"""
        upperLimit = self.imageView.upperLimit
        lowerLimit = self.imageView.lowerLimit

        # check errors
        if upperLimit is None:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Extraction error")
            dlg.setText("Upper limit is not set")
            button = dlg.exec()
            return
        if lowerLimit is None:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Extraction error")
            dlg.setText("Lower limit is not set")
            button = dlg.exec()
            return
        if lowerLimit >= upperLimit:
            dlg = QMessageBox(self)
            dlg.setWindowTitle("Extraction error")
            dlg.setText(
                "Lower limit is higher than  or equal to the upper limit\n"
                f"Lower limit: {lowerLimit}\n"
                f"Upper limit: {upperLimit}\n")
            button = dlg.exec()
            return

        # load spectrum
        self.spectrum = Spectrum.from_image(self.image, lowerLimit, upperLimit)

        # disable extract spectrum options
        for menuAction in self.extractSpectrumActions:
            menuAction.setEnabled(False)
            if menuAction.isCheckable():
                menuAction.setChecked(False)

        # enable spectrum options
        for menuAction in self.spectrumActions:
            menuAction.setEnabled(True)

        # plot spectrum
        self.spectrumView = SpectrumView(self.spectrum)
        self.setCentralWidget(self.spectrumView)

        # close image
        self.imageView.close()

    @pyqtSlot()
    def loadCalibration(self):
        """Load calibration"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "${HOME}",
            "Data (*dat);; All files (*)",
        )

        try:
            self.calibration = Calibration.from_file(filename)
        except CalibrationError as error:
            errorDialog = ErrorDialog(
                "An error occurred when loading the calibration:\n" + str(error))
            errorDialog.exec()

    @pyqtSlot()
    def openFile(self):
        """Open dialog to select and open file"""
        filename, _ = QFileDialog.getOpenFileName(
            self,
            "Open File",
            "${HOME}",
            "Fits Files (*fit *.fits *.fits.gz);; Data (*dat);; All files (*)",
        )

        # figure out whether to open an Image or a Spectrum
        file_type = getFileType(filename)

        # Unkonw extension, report message in the status bar
        if file_type is None:
            message = "Unrecognized file extension"
            self.statusBar().showMessage(message)

        # open Image
        elif file_type == "Image":
            try:
                # load image
                self.image = Image(filename)

                # plot image
                self.imageView = ImageView(self.image)
                self.setCentralWidget(self.imageView)

                # enable extract spectrum options
                for action in self.extractSpectrumActions:
                    action.setEnabled(True)

            except ImageError as error:
                errorDialog = ErrorDialog(
                    "An error occurred when opening an image:\n" + str(error))
                errorDialog.exec()

        # open Spectrum
        elif file_type == "Spectrum":
            try:
                # load spectrum
                self.spectrum = Spectrum.from_file(filename)

                # plot spectrum
                self.spectrumView = SpectrumView(self.spectrum)
                self.setCentralWidget(self.spectrumView)

                # enable spectrum options
                for menuAction in self.spectrumActions:
                    menuAction.setEnabled(True)

            except SpectrumError as error:
                errorDialog = ErrorDialog(
                    "An error occurred when opening a spectrum:\n" + str(error))
                errorDialog.exec()

    def rotateImage(self):
        """ Rotate image.

        Asks the user for the rotation angle and stores the result
        Then, rotate the image and update the plot
        """
        rotateImgageDialog = RotateImageDialog()
        if rotateImgageDialog.exec():
            try:
                self.image.rotate(rotateImgageDialog.rotateAngleQuestion.text())
            except ImageError as error:
                errorDialog = ErrorDialog(
                    "An error occurred when rotating the image:\n" + str(error))
                errorDialog.exec()
            self.imageView.setImage(self.image)

    def saveCalibration(self):
        """ Save calibration"""
        if self.calibration is None:
            errorDialog = ErrorDialog(
                "Set calibration before saving it")
            errorDialog.exec()
            return

        filename, _ = QFileDialog.getSaveFileName(
            self,
            "Save File",
            "calibration.dat",
            "Data (*dat);; All (*)")

        if filename = "":
            return
        try:
            self.calibration.save(filename)
        except CalibrationError as error:
            errorDialog = ErrorDialog(
                "An error occurred when saving the calibration:\n" + str(error))
            errorDialog.exec()

    def saveSpectrum(self):
        """ Save spectrum"""
        filename, _ = QFileDialog.getSaveFileName(
            self,
            'Save File',
            self.spectrum.name,
            "Data (*dat)")

        if filename = "":
            return
        self.spectrum.name = filename
        try:
            self.spectrum.save()
        except SpectrumError as error:
            errorDialog = ErrorDialog(
                "An error occurred when saving the spectrum:\n" + str(error))
            errorDialog.exec()

    def setCalibration(self):
        """Find the calibration solution"""
        # uncheck the other actions
        for menuAction in self.spectrumActions:
            if menuAction.isCheckable() and menuAction.isChecked():
                menuAction.setChecked(False)

        try:
            self.calibration = Calibration.from_points(
                self.spectrumView.calibrationPoints)
            successDialog = SuccessDialog("Calibration is set")
            successDialog.exec()
        except CalibrationError as error:
            errorDialog = ErrorDialog(
                "An error occurred whe setting the calibration:\n" + str(error))
            errorDialog.exec()

    def showCalibrationPoints(self):
        """ Show current calibration points

        Optionally modify them
        """
        self.spectrumView.showCalibrationPoints()
