"""Define SpectrumView widget as an extension of pg.PlotWidget"""
import numpy as np

from PyQt6.QtCore import Qt
from PyQt6.QtGui import QPen
import pyqtgraph as pg


class SpectrumView(pg.PlotWidget):
    """ Manage spectrum plotting

    Methods
    -------
    (see pg.PlotWidget)
    __init__

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

        # plot image
        self.spectrumItem = None
        self.updatePlot()

    def setPlot(self):
        """Load plot settings"""

        self.setLabel(axis='left', text='Flux')
        if self.spectrum.wavelength is None:
            self.setLabel(axis='bottom', text='X-pixel')
        else:
            self.setLabel(axis='bottom', text='Wavelength [Angs]')

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
