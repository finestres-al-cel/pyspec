import sys
import pyqtgraph as pg
import numpy as np
from PyQt6.QtWidgets import QApplication, QMainWindow


class ImageView(pg.ImageView):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.line = None
        self.image_plot = None

    def setImage(self, image):
        super().setImage(image)

        # Create the horizontal line plot item
        if self.image_plot is None:
            self.image_plot = self.getImageItem()
        if self.line is not None:
            self.plotHorizontalLine()

    def setLine(self, line):
        self.line = line
        self.plotHorizontalLine()

    def plotHorizontalLine(self):
        if self.image_plot is None:
            return

        if self.line is not None:
            height, width = self.image_plot.image.shape[:2]
            line_y = max(0, min(self.line, height - 1))
            self.image_plot.clear()
            self.image_plot.plot([0, width - 1], [line_y, line_y], pen=pg.mkPen('r'))


# Create the application
app = QApplication(sys.argv)

# Create the main window
window = QMainWindow()
window.setWindowTitle("ImageView Example")

# Create an instance of the custom ImageView widget
image_view = ImageView(window)

# Set some dummy image data for demonstration
image_data = np.random.randint(0, 255, size=(400, 300))
image_view.setImage(image_data)

# Set the line position
line_position = 200
image_view.setLine(line_position)

# Set the main window size
window.setGeometry(100, 100, 600, 400)

# Show the main window
window.show()

# Run the application's event loop
sys.exit(app.exec())
