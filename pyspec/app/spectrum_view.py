"""Define SpectrumView widget as an extension of pg.PlotWidget"""
import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen
import pyqtgraph as pg

from pyspec.app.add_calibration_point_dialog import AddCalibrationPointDialog
from pyspec.app.calibration_point_list_dialog import CalibrationPointListDialog
from pyspec.app.error_dialog import ErrorDialog

class SpectrumView(pg.PlotWidget):
    """ Manage spectrum plotting

    Methods
    -------
    (see pg.PlotWidget)
    __init__
    activateSetCalibrationPoints
    addCalibrationPoint
    deactivateSetCalibrationPoints
    mousePressEvent
    setPlot
    updatePlot

    Attributes
    ----------
    (see pg.PlotWidget)

    chooseLimit: str or None
    String that specifies which limit is being set ("upper" or "lower"). None for
    no limit. If any limit is set, then mouse clicks on the image will store
    the y position of the click

    lowerLimit: int or None
    Lower limit of the area to be considered in the extraction of a spectrum

    upperLimit: int or None
    Upper limit of the area to be considered in the extraction of a spectrum
    """
    def __init__(self, spectrum):
        """Initialize instance

        Arguments
        ---------
        spectrum: Spectrum
        The Spectrum to be shown
        """
        # initialize plotting
        super().__init__()
        self.show()

        # keep spectrum
        self.spectrum = spectrum

        # calibration points
        self.calibrationPoints = {}
        self.calibrationPointsItem = None

        # mouse control
        self.setCalibrationPoints = False

        # plot image
        self.spectrumItem = None
        self.updatePlot()


    def activateSetCalibrationPoints(self):
        """Activate on click actions to set calibration points

        Arguments
        ---------
        menuAction: QAction
        Menu action indicating the limit to be set

        Return
        ------
        statusMessage: str
        Status message with the chosen limit
        """
        self.setCalibrationPoints = True

        statusMessage = "Setting calibration points"
        return statusMessage

    def addCalibrationPoint(self, viewPos):
        """Add calibration point"""
        xPos = self.spectrum.findLocalMax(int(viewPos.x()))

        addCalibrationPointDialog = AddCalibrationPointDialog(xPos)

        if addCalibrationPointDialog.exec():
            try:
                if addCalibrationPointDialog.xPosQuestion.text() != "":
                    xPos = int(addCalibrationPointDialog.xPosQuestion.text())
            except ValueError as error:
                errorDialog = ErrorDialog("X position must be an integer")
                errorDialog.exec()
                return

            try:
                wavelength = float(addCalibrationPointDialog.wavelengthQuestion.text())
            except ValueError as error:
                errorDialog = ErrorDialog("Wavelength must be a float")
                errorDialog.exec()
                return

            self.calibrationPoints[xPos] = wavelength
            print(xPos, wavelength)

            self.updatePlot()

    def deactivateSetCalibrationPoints(self):
        """Deactivate on click actions to set calibration points

        Return
        ------
        statusMessage: str
        Empty status message
        """
        self.setCalibrationPoints = False

        statusMessage = ""
        return statusMessage

    def mousePressEvent(self, event):
        """Manage mouse press events

        Arguments
        ---------
        event: PyQt6.QtGui.QMouseEvent
        Mouse event
        """
        if event.button() == Qt.MouseButton.LeftButton and self.setCalibrationPoints:
            pos = event.pos()
            scenePos = self.mapToScene(pos)
            viewPos = self.getViewBox().mapSceneToView(scenePos)

            self.addCalibrationPoint(viewPos)

            self.updatePlot()
        else:
            super().mousePressEvent(event)

    def setPlot(self):
        """Load plot settings"""

        self.setLabel(axis='left', text='Flux')
        if self.spectrum.wavelength is None:
            self.setLabel(axis='bottom', text='X-pixel')
        else:
            self.setLabel(axis='bottom', text='Wavelength [Angs]')

    def showCalibrationPoints(self):
        """ Show current calibration points

        Optionally modify them
        """
        calibrationPointListDialog = CalibrationPointListDialog(
            self.calibrationPoints)
        if calibrationPointListDialog.exec():
            self.calibrationPoints = {
                item[0]: item[1]
                for item in calibrationPointListDialog.calibrationPoints
                if not item[2]
            }
            self.updatePlot()


    def updatePlot(self):
        """Update plot"""
        # reset plot
        self.clear()

        # load plot settings
        self.setPlot()

        # plot spectrum
        pen = pg.mkPen("r")
        if self.spectrum.wavelength is None:
            xArray = np.arange(self.spectrum.flux.size)
        else:
            xArray = self.spectrum.wavelength
        self.spectrumItem = pg.PlotCurveItem(
            xArray,
            self.spectrum.flux,
            pen=pen)
        self.addItem(self.spectrumItem)

        # plot calibration points
        if len(self.calibrationPoints) > 0:
            self.calibrationPointsItem = pg.ScatterPlotItem(
                size=10, brush=pg.mkBrush(255, 255, 255, 120))
            self.calibrationPointsItem.addPoints([
                {"pos": (index, self.spectrum.flux[index]), 'data': 1}
                for index in self.calibrationPoints
            ])
            self.addItem(self.calibrationPointsItem)
