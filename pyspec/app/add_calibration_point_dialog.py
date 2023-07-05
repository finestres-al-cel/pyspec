""" Dialog to add calibration points"""
from PyQt6.QtWidgets import (
    QDialog, QDialogButtonBox, QGridLayout, QLabel, QLineEdit
)

class AddCalibrationPointDialog(QDialog):
    """ Class to define the dialog to add a CalibrationPoint

    Methods
    -------
    (see QDialog)
    __init__

    Arguments
    ---------
    (see QDialog)

    buttonBox: QDialogButtonBox
    Accept/cancel button

    xPosQuestion: QLineEdit
    Field to modify the peak position

    wavelengthQuestion: QLineEdit
    Field to modify the wavelength of the peak
    """
    def __init__(self, xPos, wavelength=None):
        """Initialize instance

        Arguments
        ---------
        xPos: int
        Initial guess for x position
        """
        super().__init__()

        self.setWindowTitle("Add calibration point")

        QButtons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QButtons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.xPosQuestion = QLineEdit()
        self.xPosQuestion.setMaxLength(10)
        self.xPosQuestion.setPlaceholderText(str(xPos))

        self.wavelengthQuestion = QLineEdit()
        self.wavelengthQuestion.setMaxLength(10)
        if wavelength is None:
            self.wavelengthQuestion.setPlaceholderText("Enter wavelength")
        else:
            self.wavelengthQuestion.setPlaceholderText(str(wavelength))

        layout = QGridLayout()
        layout.addWidget(QLabel("wavelength (in Angs)"), 0, 0)
        layout.addWidget(self.wavelengthQuestion, 0, 1)
        layout.addWidget(QLabel("X position"), 1, 0)
        layout.addWidget(self.xPosQuestion, 1, 1)
        layout.addWidget(self.buttonBox)
        self.setLayout(layout)
