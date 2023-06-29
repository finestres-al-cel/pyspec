"""Utils file contianing useful functions"""

from pyspec.image import ACCEPTED_FORMATS as ACCEPTED_FORMATS_IMAGE
from pyspec.spectrum import ACCEPTED_FORMATS as ACCEPTED_FORMATS_SPECTRUM

def getFileType(filename):
    """Figure out if the file is an Image or a Spectrum

    Make the decision based on the filename extension

    Attributes
    ----------
    filename: str
    Name of the file

    Return
    ------
    file_type: str or None
    'Image' or 'Spectrum' if the extension is in ACCEPTED_FORMATS_IMAGE or
    ACCEPTED_FORMATS_SPECTRUM respectively. None otherwise
    """
    file_type = None
    for format in ACCEPTED_FORMATS_IMAGE:
        if filename.endswith(format):
            file_type = "Image"
    for format in ACCEPTED_FORMATS_SPECTRUM:
        if filename.endswith(format):
            file_type = "Spectrum"

    return file_type
