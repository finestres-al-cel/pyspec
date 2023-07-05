""" Basic Spectrum """
import numpy as np

from pyspec.errors import SpectrumError

ACCEPTED_FORMATS = [".dat"]

class Spectrum:
    """ Basic Spectrum

    Class methods
    -------------
    from_image
    from_file

    Methods
    -------
    __init__
    find_local_max
    save

    Attributes
    ----------
    flux: array of float
    Spectrum flux

    wavelength: array of float or None
    Spectrum wavelength. None when spectrum wavelength is not calibrated

    name: str
    Name of the file
    """
    def __init__(self, flux, wavelength, name):
        """Initialize instance

        Arguments
        ---------
        flux: array of float
        The spectrum flux

        wavelength: array of float or None
        The spectum wavelength. None it it's not calibrated

        name: str
        Name of the spectrum. E.g. name of the loaded file or suggested name
        for the saving file
        """
        self.name = name
        self.flux = flux
        self.wavelength = wavelength

    def find_local_max(self, x_pos):
        """Find the local maximum.

        This function assumes that you are giving a position close to a peak
        maximum and corrects it if necessary

        Arguments
        ---------
        x_pos: int
        Initial guess

        Returns
        -------
        x_pos: int
        The position of the peak
        """
        while True:
            if x_pos > 0 and self.flux[x_pos - 1] > self.flux[x_pos]:
                x_pos -= 1
            elif x_pos < self.flux.size - 1 and self.flux[x_pos + 1] > self.flux[x_pos]:
                x_pos += 1
            else:
                return x_pos


    @classmethod
    def from_image(cls, image, lower_limit, upper_limit):
        """Create a Spectrum from an Image

        Arguments
        ---------
        image: Image
        Image from which to extract the spectrum

        lower_limit: int
        Lower limit of the extraction region. Must be smaller than upper_limit

        upper_limit: int
        Upper limit of the extraction region. Must be smaller than lower_limit

        Return
        ------
        spectrum: Spectrum
        The initialized spectrum
        """
        name = image.filename.replace(
            image.image_extension, "_extracted.dat")
        flux = np.mean(image.data[lower_limit: upper_limit, :], axis=0)
        wavelength = None

        return cls(flux, wavelength, name)

    @classmethod
    def from_file(cls, filename):
        """Load a Spectrum from file

        Arguments
        ---------
        filename: str
        The name of the file

        Return
        ------
        spectrum: Spectrum
        The initialized spectrum

        Raise
        -----
        SpectrumError if the file content was not correct
        """
        data = np.genfromtxt(filename, names=True)

        try:
            flux = data["flux"]
            if "wavelength[Angstroms]" in data.dtype.names:
                wavelength = data["wavelength[Angstroms]"]
            else:
                wavelength = None
        except ValueError as error:
            raise SpectrumError(
                f"Spectrum: 'filename' has incorrect content: {str(error)}"
                ) from error

        return cls(flux, wavelength, filename)

    def save(self):
        """Save spectrum

        Raise
        -----
        SpectrumError if the filename does not have the correct format
        """
        # check filename extension
        extension = None
        for format_check in ACCEPTED_FORMATS:
            if self.name.endswith(format_check):
                extension = format_check
        if extension is None:
            raise SpectrumError(
                "Spectrum: 'name' has incorrect extension. Valid"
                "extensions are " + ", ".join(ACCEPTED_FORMATS)
                )

        with open(self.name, "w", encoding="UTF-8") as file:
            if self.wavelength is None:
                file.write("# flux\n")
                for flux in self.flux:
                    file.write(f"{flux}\n")
            else:
                file.write("# wavelength[Angstroms] flux\n")
                for flux, wavelength in zip(self.flux, self.wavelength):
                    file.write(f"{wavelength} {flux}\n")
