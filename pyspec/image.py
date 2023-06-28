""" Basic Image """
from astropy.io import fits

from pyspec.errors import ImageError

ACCEPTED_FORMATS = ["fit", "fits", "fits.gz"]

class Image:
    """ Basic Image

    Methods
    -------
    __init__

    Attributes
    ----------
    data: array of float
    The image data

    filename: str
    Name of the file containing the image

    header: astropy.io.fits.header.Header
    The image header
    """
    def __init__(self, filename):
        """Initialize instance

        Arguments
        ---------
        filename: str
        Filename to open

        Raise
        -----
        ImageError if filename is not a string
        ImageError if filename does not have the correct format
        """
        # check filename type
        if not isinstance(filename, str):
            raise ImageError(
                f"Image: Argument 'filename' has incorrect type. Expected string "
                f"found {type(filename)}. {filename}")

        # check filename extension
        format_ok = False
        for format in ACCEPTED_FORMATS:
            if filename.endswith(format):
                format_ok = True
        if not format_ok:
            raise ImageError(
                f"{self.__name__}: 'filename' has incorrect extension. Valid"
                "extensions are " + ", ".join(ACCEPTED_FORMATS)
                )

        try:
            hdu = fits.open(filename)
        except IOError as error:
            raise SpectrumFileError(my_name, str(error)) from error

        self.filename = filename
        self.header = hdu[0].header
        self.data = hdu[0].data

        hdu.close()
