"""Dialog to show the list of calibration points"""
from PyQt6 import QtCore, QtGui, sip
from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit, QPushButton, QVBoxLayout
)

from pyspec.app.add_calibration_point_dialog import AddCalibrationPointDialog
from pyspec.app.q_push_button_index import QPushButtonIndex

class CalibrationPointListDialog(QDialog):
    """ Class to define the dialog to list and modify current calibration point

    Methods
    -------
    (see QDialog)
    __init__

    Arguments
    ---------
    (see QDialog)

    buttonBox: QDialogButtonBox
    Accept/cancel button

    calibrationPoints: list of [int, float, boolean]
    List with lists containting:
    1. An integer with the x position of the peak
    2. A float with the wavelength of the peak
    3. A boolean determining whether this peak has been deleted (True) or not (False)
    """
    def __init__(self, calibrationPoints):
        """Initialize instance

        Arguments
        ---------
        calibrationPoints: dict
        Dictionary with pairs of x and wavelengths
        """
        super().__init__()

        self.calibrationPoints = [
            [key, calibrationPoints.get(key), False]
            for key in sorted(calibrationPoints)
        ]

        self.setWindowTitle("Calibration points list")

        self.updateLayout()

    def deletePoint(self):
        """Mark point as deleted"""
        index = self.sender().index
        self.calibrationPoints[index][2] = True
        self.updateLayout()

    def modifyPoint(self):
        """Modify selected point"""
        index = self.sender().index

        xPos, wavelength, _ = self.calibrationPoints[index]

        # ask for new values
        addCalibrationPointDialog = AddCalibrationPointDialog(xPos, wavelength)
        if addCalibrationPointDialog.exec():
            try:
                if addCalibrationPointDialog.xPosQuestion.text() != "":
                    xPos = int(addCalibrationPointDialog.xPosQuestion.text())
            except ValueError as error:
                self.statusBar().showMessage(
                    "X position must be an integer"
                )

            try:
                if addCalibrationPointDialog.wavelengthQuestion.text() != "":
                    wavelength = float(addCalibrationPointDialog.wavelengthQuestion.text())
            except ValueError as error:
                self.statusBar().showMessage(
                    "X position must be a float"
                )

            # update values
            self.calibrationPoints[index][0] = xPos
            self.calibrationPoints[index][1] = wavelength

            self.updateLayout()

    def restorePoint(self):
        """Restore point marked as deleted"""
        index = self.sender().index
        self.calibrationPoints[index][2] = False
        self.updateLayout()

    def updateLayout(self):
        """Update the dialog layout"""
        currentLayout = self.layout()
        if currentLayout is not None:
            while currentLayout.count():
                item = currentLayout.takeAt(0)
                widget = item.widget()
                if widget is not None:
                    widget.deleteLater()
                else:
                    self.deleteLayout(item.layout())
            sip.delete(currentLayout)

        # empty list of points
        if len(self.calibrationPoints) == 0:
            QButtons = QDialogButtonBox.StandardButton.Ok

            self.buttonBox = QDialogButtonBox(QButtons)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            layout = QVBoxLayout()
            layout.addWidget(QLabel("No peaks found"))
            layout.addWidget(self.buttonBox)

        # list with items
        else:
            QButtons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

            self.buttonBox = QDialogButtonBox(QButtons)
            self.buttonBox.accepted.connect(self.accept)
            self.buttonBox.rejected.connect(self.reject)

            layout = QGridLayout()
            layout.addWidget(QLabel("X position"), 0, 0)
            layout.addWidget(QLabel("wavelength"), 0, 1)
            layout.addWidget(QLabel("(in Angs)"), 1, 1)

            next_index = 2
            for index, (xPos, wavelength, deleted) in enumerate(self.calibrationPoints):
                if deleted:
                    labelXPos = QLabel(str(xPos))
                    font = labelXPos.font()
                    font.setItalic(True)
                    font.setStrikeOut(True)
                    labelXPos.setFont(font)
                    labelXPos.setStyleSheet("color: red")
                    layout.addWidget(labelXPos, index + next_index, 0)

                    labelWavelength = QLabel(str(wavelength))
                    font = labelWavelength.font()
                    font.setItalic(True)
                    font.setStrikeOut(True)
                    labelWavelength.setFont(font)
                    labelWavelength.setStyleSheet("color: red")
                    layout.addWidget(labelWavelength, index + next_index, 1)

                    restoreButton = QPushButtonIndex("Restore", index)
                    restoreButton.clicked.connect(self.restorePoint)
                    layout.addWidget(restoreButton, index + next_index, 2)

                else:
                    layout.addWidget(QLabel(str(xPos)), index + next_index, 0)
                    layout.addWidget(QLabel(str(wavelength)), index + next_index, 1)

                    deleteButton = QPushButtonIndex("Delete", index)
                    deleteButton.clicked.connect(self.deletePoint)
                    layout.addWidget(deleteButton, index + next_index, 2)

                    modifyButton = QPushButtonIndex("Modify", index)
                    modifyButton.clicked.connect(self.modifyPoint)
                    layout.addWidget(modifyButton, index + next_index, 3)


            next_index += index + 1
            layout.addWidget(self.buttonBox, next_index, 4)

        self.setLayout(layout)
