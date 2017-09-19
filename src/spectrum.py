"""
    This module contains the definition of the class Spectrum, its methods, and associated constants
    
    MODULE: spectrum
    FILE: spectrum.py
    CLASSES: Spectrum
    USES: SpectrumFormatError, SpectrumTypeError
    
    MINIMUM REQUIREMENTS:
    * astropy 1.3
    * maptlotlib 2.0.0
    * scipy 0.18.1
    
    AUTHOR: Ignasi Perez-Rafols (iprafols@gmail.com)
    VERSION: 1.0
    
    """
__version__ = '1.0'
__version__astropy = '1.3'
__version__matplotlib = '2.0.0'
__version__scipy = '0.18.1'

import astropy.io.fits as fits
from enum import Enum
import matplotlib.pyplot as plt
import matplotlib.gridspec as gridspec
from matplotlib.backend_bases import MouseEvent, KeyEvent
import numpy as np
from scipy.ndimage import rotate, shift

from errors.spectrum_format_error import SpectrumFormatError
from errors.spectrum_name_error import SpectrumNameError
from errors.spectrum_type_error import SpectrumTypeError
from errors.spectrum_file_error import SpectrumFileError

# figure settings
FIGSIZE_SQUARE = (7, 7)
FIGSIZE_HORIZONTAL = (14, 7)
FONTSIZE = 24
CMAP = plt.cm.get_cmap('Greys_r')

# image formats accepted
FORMATS = ["fit", "fits"]
# TODO: add camera raw images
class FormatType(Enum):
    IMAGE = 1
    DATA = 2

class SelectLine(Enum):
    TOP = 1
    BOTTOM = 2
    NONE = 3


class Spectrum(object):
    """
        Manage the spectrum data
        
        CLASS: Spectrum
        PURPOSE: Manage the spectrum data. In particular, extract the spectrum from the raw image,
                 and calibrate the wavelength
        PUBLIC METHODS:
        __init__                : Initialize class instance
        extract                 : Extract the spectrum
        plotRawSpectrum         : Plot the uncalibrated spectrum
        plotCalibratedSpectrum  : Plot the calibrated spectrum
        
        PRIVATE METHODS (should not be accessed outside the class):
        __addLine               : Add a horizontal line to the raw image plot to signal the extraction 
                                  area
        __currentStatus         : Print text describing the current status
        __extract               : Extract the spectrum in the selected region
        __rotateImage           : Rotate the image
        __saveSpectrum        : Save the extracted spectrum
        __selectEvent           : React to a key event calling the appropiate function
        
        PERMANENT PRIVATE MEMBERS (should not be accessed outside the class):
        __calibrated (bool) : True if the spectrum has been calibrated, False otherwise
        __extracted (bool)  : True if the spectrum has been extracted from the raw image
                              or loaded directly, False otherwise
        __has_image (bool)  : True if a raw image has been loaded
        __name (string)     : Name of the spectrum (without extension)
        
        TRANSIENT PRIVATE MEMBERS (should not be accessed outside the class, and should be checked 
            before usage):
        __ax (matplotlib.axes._subplots.AxesSubplot)  : primary axis to plot things
        __ax0 (matplotlib.axes._subplots.AxesSubplot) : auxiliar axis to plot figure status 
                                                        and capabilities
        __bottomline (matplotlib.lines.Line2D)        : horizontal line to select the bottom limit
                                                        of the area to be considered in the extraction
                                                        of a spectrum
        __gs (gridspec.GridSpec)                      : grid to place the axes
        __imshow (matplotlib.image.AxesImage)         : data image
        __status_text (string)                        : text displayed in __ax0 to let the user know
                                                        the status of the plot
        __spectrum (np.ndarray)                       : an array containing the extracted spectrum
        __topline (matplotlib.lines.Line2D)           : horizontal line to select the top limit
                                                        of the area to be considered in the extraction
                                                        of a spectrum
        __whichLine (SelectLine)                      : active line (__bottomline, __topline or None)
        __ybottom (int)                               : y value of __bottomline
        __ytop (int)                                  : y value of __topline
        __wavelength (np.ndarray)                     : calibrated wavelength for the spectrum
        
        """
    
    def __init__(self, image_name):
        """
            Initialize class instance
            
            METHOD: Spectrum.__init__
            TYPE: Constructor, public
            
            PURPOSE: 
            Initialize class instance. In particular, keep the image name (without extension)
            and read the data. Initialize control variables (__extracted, __calibrated)
            If the image name ends with '_extracted.txt', then it is assumed to be a data file 
            with the spectrum information. First line of the file must be either '# spectrum' or
            '# wavelength(Angs) spectrum'.
            
            ARGUMENTS:
            image_name (string) : Filename of the image. Must be in one of the formats specified 
                                  in FORMATS
            RETURNS:
            An instance of Spectrum
            
            RAISES:
            * SpectrumFormatError when the given format is not found in FORMATS
            * SpectrumTypeError when the arguments are of incorrect type
            
            EXAMPLES:
            * spec = Spectrum('test_image.fits')
            
            """
        my_name = '__init__'
        # check argument type
        if not (type(image_name) == str):
            raise SpectrumTypeError(my_name, "Argument 'image_name' has incorrect type")
        
        # check file extension
        check_format = False
        for item in FORMATS:
            if image_name.endswith(item):
                check_format = True
                file_type = FormatType.IMAGE
            if not check_format and image_name.endswith("_extracted.dat"):
                check_format = True
                file_type = FormatType.DATA
        if not check_format:
            raise SpectrumFormatError(my_name, "Image format not supported, accepted formats: {}".format(", ".join(FORMATS)))
        del check_format

        # keep image name without extension
        if file_type == FormatType.IMAGE:
            self.__name = image_name[:image_name.rfind('.')]
        elif file_type == FormatType.DATA:
            self.__name = image_name[:image_name.rfind('_')]
        else:
            raise SpectrumFormatError(my_name, "Invalid value for FormatType")
    
        # read data and initialize control variables
        if file_type == FormatType.IMAGE:
            try:
                im = fits.open(image_name)
            except IOError as e:
                raise SpectrumFileError(my_name, str(e))
            self.__data = im[0].data
            im.close()

            self.__has_image = True
            self.__extracted = False
            self.__calibrated = False
                
        elif file_type == FormatType.DATA:
            self.__has_image = False
            try:
                data = np.genfromtxt(image_name, names=True)
            except IOError as e:
                raise SpectrumFileError(my_name, str(e))
            try:
                self.__spectrum = data["spectrum"]
                self.__extracted = True
            except ValueError:
                raise SpectrumFormatError(my_name, "Data file has invalid format")
            try:
                self.__wavelength = data["wavelength(Angs)"]
                self.__calibrated = True
            except ValueError:
                self.__calibrated = False
    
        else:
            raise SpectrumFormatError(my_name, "Invalid value for FormatType")
    
    def __addLine(self, event):
        """
            Add a horizontal line to the raw image plot to signal the extraction area
            
            METHOD: Spectrum.__addLine
            TYPE: Private
            
            PURPOSE:
            Add a horizontal line to the raw image plot to signal the extraction area. 
            The line to be set is stored in the transient member __whichline, which should
            be present. If __whichline is set to SelectLine.NONE, do nothing
            
            ARGUMENTS:
            event (MouseEvent) : Event with the y position of the line to plot
            
            RETURNS:
            NONE
            
            RAISES:
            * SpectrumNameError when one or more of __whichline, __ybottom, __ytop, __bottomline,
                __topline, or __ax are missing.
            * SpectrumTypeError when the arguments are of incorrect type
            
            EXAMPLES:
            * ax.figure.canvas.mpl_connect('button_press_event', self.__addLine)
            
            """
        my_name = '__addLine'
        # check arguments type
        if not isinstance(event, MouseEvent):
            plt.close()
            raise SpectrumTypeError(my_name, "Argument 'event' has incorrect type")
        
        # check that transient members are present
        if not (hasattr(self, "_Spectrum__whichline") and hasattr(self, "_Spectrum__ybottom") and hasattr(self, "_Spectrum__ytop") and hasattr(self, "_Spectrum__bottomline") and hasattr(self, "_Spectrum__topline") and hasattr(self, "_Spectrum__ax")):
            raise SpectrumNameError(my_name, "One or more of  __whichline, __ybottom, __ytop, __bottomline, __topline, or __ax are missing.")
        
        # add line
        if self.__whichline == SelectLine.BOTTOM:
            self.__ybottom = int(event.ydata)
            self.__bottomline.set_data(self.__ax.get_xlim(), np.array([event.ydata, event.ydata]))
        elif self.__whichline == SelectLine.TOP:
            self.__ytop = int(event.ydata)
            self.__topline.set_data(self.__ax.get_xlim(), np.array([event.ydata, event.ydata]))
        self.__ax.figure.canvas.draw()

    def __currentStatus(self):
        """
            Print text describing the current status
            
            METHOD: Spectrum.__currentSatus
            TYPE: Private
            
            PURPOSE:
            Print text describing the current status. In particular, print a different message
            according to the value of __whichline.
            
            ARGUMENTS:
            NONE
            
            RETURNS:
            NONE
            
            RAISES:
            * SpectrumNameError when one or more of  __whichline, __status_text or __ax0 are missing.
            
            EXAMPLES:
            * self.__currentStatus()
            
            """
        my_name = '__currentStatus'
        # check that transient members are present
        if not (hasattr(self, "_Spectrum__whichline") and hasattr(self, "_Spectrum__status_text") and hasattr(self, "_Spectrum__ax0")):
            plt.close()
            raise SpectrumNameError(my_name, "One or more of __whichline, __status_text or __ax0 are missing.")
        
        # print current status
        self.__status_text.remove()
        if self.__whichline == SelectLine.TOP:
            text = "click to set top line"
        elif self.__whichline == SelectLine.BOTTOM:
            text = "click to set bottom line"
        else:
            text = ""
        self.__status_text = self.__ax0.text(1.0, 0.5, text, horizontalalignment='right', verticalalignment='center', transform=self.__ax0.transAxes, fontsize=15)
        self.__ax0.figure.canvas.draw()

    def __extract(self):
        """
            Extract the spectrum in the selected region
            
            METHOD: Spectrum.__extract
            TYPE: Private
            
            PURPOSE:
            Extract the spectrum in the region between the horizontal lines __ytop and __ybottom,
            save the spectrum.
            
            ARGUMENTS:
            NONE
            
            RETURNS:
            NONE
            
            RAISES:
            * SpectrumNameError when one or more of  __ytop or __ybottom are missing.
            * SpectrumExtractionError when __ytop is lower than __ybottom
            
            EXAMPLES:
            * self.__extract()
            
            """
        my_name = '__extract'
        # check that transient members are present
        if not (hasattr(self, "_Spectrum__ytop") and hasattr(self, "_Spectrum__ybottom")):
            plt.close()
            raise SpectrumNameError(my_name, "One or more of __ytop or __ybottom are missing.")
        
        # check that __ytop is higher than __ybottom
        if self.__ytop < self.__ybottom:
            plt.close()
            raise SpectrumExtractionError(my_name, "Could not extract: top line below bottom line")
        
        # extract spectrum
        self.__spectrum = np.mean(self.__data[self.__ybottom:self.__ytop,:], axis=0)
        self.__extracted = True
            
    def __rotateImage(self):
        """
            Rotate the image
            
            METHOD: Spectrum.__rotateImage
            TYPE: Private
            
            PURPOSE:
            Rotate the image, then display it again.
            
            ARGUMENTS:
            NONE
            
            RETURNS:
            NONE
            
            RAISES:
            * SpectrumNameError when one or more of __ax or __imshow are missing.
            
            EXAMLES:
            * self.__rotateImage()
            
            """
        # TODO: enable angle entry from plotting interface
        my_name = '__rotateImage'
        # check that transient members are present
        if not (hasattr(self, "_Spectrum__ax") and hasattr(self, "_Spectrum__imshow")):
            plt.close()
            raise SpectrumNameError(my_name, "One or more of __ax or __imshow are missing.")
        
        # get rotation angle and then rotate the image around the specified center
        rot_angle_found = False
        while not rot_angle_found:
            try:
                rot_angle = float(raw_input("Please enter the rotation angle (in degrees, positive for clockwise rotation) -->"))
                rot_angle_found = True
            except ValueError:
                pass
        del rot_angle_found
    
        # rotate data
        if rot_angle == 0.0:
            return
        self.__data = rotate(self.__data, rot_angle)
        
        # update plot
        self.__imshow.remove()
        del self.__imshow
        self.__imshow = self.__ax.imshow(self.__data, cmap=CMAP, origin='lower')
        self.__ax.figure.canvas.draw()

    def __saveSpectrum(self):
        """
            Save the extracted spectrum
            
            METHOD: Spectrum.__saveSpectrum
            TYPE: Private
            
            PURPOSE:
            Save the extracted spectrum. The name of the file is the same as the input file, 
            but with the extension replaced by '_extracted.dat' appended to it. If __extracted is not set, then do nothing.
            If __calibrated is set, then also save the associated wavelength
            
            ARGUMENTS:
            NONE
            
            RETURNS:
            NONE
            
            RAISES:
            * SpectrumNameError when __spectrum is missing and __extracted is set.
            * SpectrumNameError when __wavelength is missing and __calibrated is set
            
            EXAMPLES:
            * self.__saveSpectrum()
            
            """
        my_name = '__saveSpectrum'
        
        # check that transient members are present
        if not hasattr(self, "_Spectrum__spectrum") and self.__extract:
            raise SpectrumNameError(my_name, "__spectrum is missing.")
        if not hasattr(self, "_Spectrum__wavelength") and self.__calibrated:
            raise SpectrumNameError(my_name, "__wavelength is missing.")
        
        # return if __extracted is not set
        if not self.__extracted:
            return
        
        # save the spectrum
        f = open("{}_extracted.dat".format(self.__name), 'w')
        # if calibration is not done, save the spectrum
        if not self.__calibrated:
            f.write("# spectrum\n")
            [f.write("{}\n".format(s)) for s in self.__spectrum]
        # otherwise save the spectrum and the calibration
        else:
            f.write("# wavelength(Angs) spectrum\n")
            [f.write("{} {}\n".format(w, s)) for w, s in zip(self.__wavelength, self.__spectrum)]

        f.close()
            
    
    def __selectEvent(self, event):
        """
            React to a key event calling the appropiate function
            
            METHOD: Spectrum.__selectEvent
            TYPE: Private
            
            PURPOSE:
            React to a key event calling the appropiate function. Reactions include setting which
            horizontal line to draw and rotating the image
            
            ARGUMENTS:
            event (KeyEvent) : Event with the pressed key
            
            RETURNS:
            NONE
            
            RAISES:
            * SpectrumTypeError when the arguments are of incorrect type
            
            EXAMPLES:
            * self.__ax.figure.canvas.mpl_connect('key_press_event', self.__selectEvent)
            
            """
        my_name = '__selectEvent'
        # check arguments type
        if not isinstance(event, KeyEvent):
            plt.close()
            raise SpectrumTypeError(my_name, "Argument 'event' has incorrect type")
        
        # event selected: rotation
        if event.key == "r":
            self.__rotateImage()
            return
        # event selected: select lines
        elif event.key == "t":
            self.__whichline = SelectLine.TOP
        elif event.key == "b":
            self.__whichline = SelectLine.BOTTOM
        # event selected: extract
        elif event.key == "e":
            self.__extract()
            plt.close()
            return
        # event selected: quit
        elif event.key == "q":
            plt.close()
            return
        else:
            self.__whichline = SelectLine.NONE
        # update figure
        self.__currentStatus()

    def extract(self):
        """
            Extract the spectrum
            
            METHOD: Spectrum.extract()
            TYPE: Public
            
            PURPOSE:
            Extract the spectrum. In partiuclar, plot the current image and, upon user input, rotate 
            the image, and select the extracting before extracting the spectrum. Keep the extracted
            spectrum in __spectrum and save it to disk
            
            ARGUMENTS:
            NONE
            
            RETURNS:
            A string indicating the success or failure of the extraction
            
            EXAMPLES:
            * message = spec.extract()
            
            """
        # check that there is an image to extract the spectrum from
        if not self.__has_image:
            return "There is no image to extract from"
        
        # create figure
        self.__fig = plt.figure(figsize=FIGSIZE_SQUARE)
        self.__gs = gridspec.GridSpec(2, 1, height_ratios=[1,10])
        self.__gs.update(hspace=0.2, bottom=0.1)
        
        # draw legend
        self.__ax0 = self.__fig.add_subplot(self.__gs[0])
        self.__ax0.text(0.0, 0.5, "r: rotate\nt: set top line\nb: set bottom line\ne: extract\nq: quit", horizontalalignment='left', verticalalignment='center', transform=self.__ax0.transAxes, fontsize=15)
        self.__status_text = self.__ax0.text(1.0, 0.5, "", horizontalalignment='right', verticalalignment='center', transform=self.__ax0.transAxes, fontsize=15)
        self.__ax0.axis('off')
        
        # draw empty lines, then plot image
        self.__ax = self.__fig.add_subplot(self.__gs[1])
        self.__whichline = SelectLine.NONE
        self.__ytop = -1
        self.__topline, = self.__ax.plot([0], [0], linewidth=1, linestyle='solid', color='red')
        self.__ybottom = 0
        self.__bottomline, = self.__ax.plot([0], [0], linewidth=1, linestyle='solid', color='green')
        self.__imshow = self.__ax.imshow(self.__data, cmap=CMAP, origin='lower')
        self.__ax.set_xlabel("x pixel")
        self.__ax.set_ylabel("y pixel")
        
        # add functionality
        try:
            self.__ax.figure.canvas.mpl_connect('button_press_event', self.__addLine)
            self.__ax.figure.canvas.mpl_connect('key_press_event', self.__selectEvent)
            plt.show()
        except SpectrumError as e:
            plt.close()
            raise e
        
        # save extracted spectrum and clean up memory
        if self.__extracted:
            self.__saveSpectrum()
            del self.__fig, self.__ax, self.__ax0, self.__gs, self.__status_text, self.__topline, self.__bottomline, self.__whichline, self.__ytop, self.__ybottom, self.__imshow
            return "Extraction success"
        else:
            del self.__fig, self.__ax, self.__ax0, self.__gs, self.__status_text, self.__topline, self.__bottomline, self.__whichline, self.__ytop, self.__ybottom, self.__imshow
            return "Extraction failed"

    def plotRawSpectrum(self):
        """
            Plot the uncalibrated spectrum
            
            METHOD: Spectrum.plotRawSpectrum
            TYPE: Public
            
            PRUPOSE:
            Plot the number of counts in the spectrum against the number of pixel
            
            ARGUMENTS:
            NONE
            
            RETUNRS:
            An empty string upon success or an error message
            
            RAISES:
            * SpectrumNameError when __spectrum is missing.
            """
    
        # check that the spectrum is already extracted
        if not self.__extracted:
            return "Extract spectrum first"
        
        # check that transient members are present
        if not (hasattr(self, "_Spectrum__spectrum")):
            raise SpectrumNameError(my_name, "__spectrum is missing.")
        
        # create figure
        self.__fig = plt.figure(figsize=FIGSIZE_HORIZONTAL)
        self.__gs = gridspec.GridSpec(1, 1)
        self.__gs.update(bottom=0.1)

        # draw empty lines, then plot image
        self.__ax = self.__fig.add_subplot(self.__gs[0])
        self.__ax.plot(self.__spectrum)
        self.__ax.set_xlabel("x pixel", fontsize=FONTSIZE)
        self.__ax.set_ylabel("intensity", fontsize=FONTSIZE)
        self.__ax.tick_params()
        plt.show()

        # clean up memory
        del self.__fig, self.__ax
        return ""

    def plotCalibratedSpectrum(self):
        """
            Plot the calibrated spectrum
            
            METHOD: Spectrum.plotRawSpectrum
            TYPE: Public
            
            PRUPOSE:
            Plot the number of counts in the spectrum against wavelength
            
            ARGUMENTS:
            NONE
            
            RETUNRS:
            An empty string upon success or an error message
            
            # check that transient members are present
            # TODO: add check
            """

        if not self.__extracted:
            return "Extract spectrum first"
        if not self.__calibrated:
            return "Calibrate first"
        
        # create figure
        self.__fig = plt.figure(figsize=FIGSIZE_HORIZONTAL)
        self.__gs = gridspec.GridSpec(1, 1)
        self.__gs.update(bottom=0.1)
        
        # draw empty lines, then plot image
        self.__ax = self.__fig.add_subplot(self.__gs[0])
        self.__ax.plot(self.__wavelength, self.__spectrum)
        self.__ax.set_xlabel(r"wavelength $\left(\AA\right)$", fontsize=FONTSIZE)
        self.__ax.set_ylabel("intensity", fontsize=FONTSIZE)
        plt.show()
        
        # clean up memory
        del self.__fig, self.__ax
        return ""
