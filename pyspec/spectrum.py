""" Basic Spectrum """
import numpy as np

ACCEPTED_FORMATS = ["fit", "fits", "fits.gz"]

class Spectrum:
    """ Basic Spectrum

    Methods
    -------
    __init__

    Attributes
    ----------
    flux: array of float
    Spectrum flux

    wavelength: array of float or None
    Spectrum wavelength. None when spectrum wavelength is not calibrated

    name: str
    Name of the file
    """
    def __init__(self, image, lower_limit, upper_limit):
        """Initialize instance

        Arguments
        ---------
        image: Image
        Image from which to extract the spectrum

        lower_limit: int
        Lower limit of the extraction region. Must be smaller than upper_limit

        upper_limit: int
        Upper limit of the extraction region. Must be smaller than lower_limit

        Raise
        -----
        """
        self.name = image.filename.replace(
            image.image_extension, "_extracted.dat")

        self.flux = np.mean(image.data[lower_limit: upper_limit, :], axis=0)
        self.wavelength = None
