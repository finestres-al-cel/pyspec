""" Basic Image """
from astropy.io import fits
from scipy.ndimage import rotate

from pyspec.errors import ImageError

ACCEPTED_FORMATS = [".fit", ".fits", ".fits.gz"]

class Image:
    """ Basic Image

    Methods
    -------
    __init__
    rotate

    Attributes
    ----------
    data: array of float
    The current image data

    filename: str
    Name of the file containing the image

    header: astropy.io.fits.header.Header
    The image header

    image_extension: str
    Extension of the loaded file

    original_data: array of float
    The original image data

    rotation_angle: float
    Current rotation angle. This is the sum of all rotation angles applied
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
        self.image_extension = None
        for format in ACCEPTED_FORMATS:
            if filename.endswith(format):
                self.image_extension = format
        if self.image_extension is None:
            raise ImageError(
                f"Image: 'filename' has incorrect extension. Valid"
                "extensions are " + ", ".join(ACCEPTED_FORMATS)
                )

        try:
            hdu = fits.open(filename)
        except IOError as error:
            raise SpectrumFileError(my_name, str(error)) from error

        self.filename = filename
        self.header = hdu[0].header
        self.data = hdu[0].data
        self.original_data = self.data.copy()

        self.rotation_angle = 0.0

        hdu.close()

    def rotate(self, rotation_angle_str):
        """Rotate image

        Keep the original image and the rotation angle. Further calls to this
        function will update the value of the rotation angle and rotate from
        the original data.

        Add a comment in the header

        Arguments
        ---------
        rotation_angle_str: str
        The rotation angle as a string

        Raise
        -----
        ImageError when the string does not contain a float
        """
        try:
            rotation_angle = float(rotation_angle_str)
        except ValueError as error:
            raise ImageError(
                "Image: rotation angle must be a float. Found "
                f"{rotation_angle_str}") from error

        self.rotation_angle += rotation_angle
        print(self.rotation_angle)
        self.header["COMMENTS"] = (
            f"Pyspec: Image rotated by {rotation_angle} degrees")

        if self.rotation_angle == 0.0:
            self.data = self.original_data.copy()
        else:
            self.data = rotate(self.original_data, self.rotation_angle)
