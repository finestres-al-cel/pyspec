"""Define ImageView widget as an extension of pg.ImageView"""
import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen
import pyqtgraph as pg


class ImageView(pg.PlotWidget):
    """ Manage image plotting

    Methods
    -------
    (see pg.ImageView)
    __init__
    activateChooseLimitOnClick
    deactivateChooseLimitOnClick
    mousePressEvent

    Attributes
    ----------
    (see pg.ImageView)

    chooseLimit: str or None
    String that specifies which limit is being set ("upper" or "lower"). None for
    no limit. If any limit is set, then mouse clicks on the image will store
    the y position of the click

    lowerLimit: int or None
    Lower limit of the area to be considered in the extraction of a spectrum

    upperLimit: int or None
    Upper limit of the area to be considered in the extraction of a spectrum
    """
    def __init__(self, image):
        """Initialize instance

        Arguments
        ---------
        image: Image
        The Image to be shown
        """
        # initialize plotting
        super().__init__()
        self.show()

        # keep image
        self.imageData = image.data
        self.imageShape = image.data.shape

        # limits to extract the spectrum
        self.chooseLimit = None
        self.lowerLimit = None
        self.upperLimit = None

        # plot image
        self.imageItem = None
        self.lowerLimitItem = None
        self.upperLimitItem = None
        self.updatePlot()

        # do not plot ROI and menu
        #self.ui.roiBtn.hide()
        #self.ui.menuBtn.hide()


    def activateChooseLimitOnClick(self, menuAction):
        """Activate on click actions

        Arguments
        ---------
        menuAction: QAction
        Menu action indicating the limit to be set

        Return
        ------
        statusMessage: str
        Status message with the chosen limit
        """
        if "bottom" in menuAction.text().lower():
            self.chooseLimit = "upper"
        if "top" in menuAction.text().lower():
            self.chooseLimit = "lower"

        statusMessage = f"Setting {self.chooseLimit} limit"
        return statusMessage

    def deactivateChooseLimitOnClick(self):
        """Deactivate on click actions

        Return
        ------
        statusMessage: str
        Empty status message
        """
        self.chooseLimit = None

        return ""

    def mousePressEvent(self, event):
        """Manage mouse press events

        Arguments
        ---------
        event: PyQt6.QtGui.QMouseEvent
        Mouse event
        """
        if event.button() == Qt.MouseButton.LeftButton and self.chooseLimit is not None:
            pos = event.pos()
            scene_pos = self.mapToScene(pos)
            view_pos = self.getViewBox().mapSceneToView(scene_pos)
            print("Clicked at x={}, y={}".format(view_pos.x(), view_pos.y()))

            if self.chooseLimit == "upper":
                self.upperLimit = view_pos.y()
            elif self.chooseLimit == "lower":
                self.lowerLimit = view_pos.y()

            self.updatePlot()

    def setImage(self, image):
        self.imageData = image.data
        self.imageShape = image.data.shape
        self.updatePlot()

    def setPlot(self):
        # add label
        self.setLabel(axis='left', text='Y-pixel')
        self.setLabel(axis='bottom', text='X-pixel')

    def updatePlot(self):
        self.clear()
        self.imageItem = pg.ImageItem(self.imageData)
        self.addItem(self.imageItem)

        if self.lowerLimit is not None:
            pen = pg.mkPen("r")
            self.lowerLimitItem = pg.InfiniteLine(
                angle=0, movable=False, pen=pen)
            self.lowerLimitItem.setPos(self.lowerLimit)
            #self.lowerLimitItem.setPen(QPen(Qt.GlobalColor.red))
            self.addItem(self.lowerLimitItem)

        if self.upperLimit is not None:
            pen = pg.mkPen("g")
            self.upperLimitItem = pg.InfiniteLine(
                angle=0, movable=False, pen=pen)
            self.upperLimitItem.setPos(self.upperLimit)
            self.addItem(self.upperLimitItem)