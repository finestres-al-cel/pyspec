from PyQt6.QtWidgets import QDialog, QDialogButtonBox, QVBoxLayout, QLineEdit

class RotateImageDialog(QDialog):
    """ Class to define the dialog to rotate an Image

    Methods
    -------
    __init__

    Arguments
    ---------

    """
    def __init__(self):
        """Initialize instance"""
        super().__init__()

        self.setWindowTitle("Rotate image")

        QButtons = QDialogButtonBox.StandardButton.Ok | QDialogButtonBox.StandardButton.Cancel

        self.buttonBox = QDialogButtonBox(QButtons)
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        self.rotateAngleQuestion = QLineEdit()
        self.rotateAngleQuestion.setMaxLength(10)
        self.rotateAngleQuestion.setPlaceholderText("Enter rotation angle")

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.rotateAngleQuestion)
        self.layout.addWidget(self.buttonBox)
        self.setLayout(self.layout)
