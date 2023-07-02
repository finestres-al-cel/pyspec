"""Calibration class """
import numpy as np

from pyspec.errors import CalibrationError

MIN_CALIBRATION_POINTS = 5
ACCEPTED_FORMATS = [".dat"]

class Calibration():
    """Computes and stores the wavelength solution for flux calibration

    Clas methods
    ------------
    from_file

    Methods
    -------
    __init__

    Attributes
    ----------
    calibration_points: np.ndarray
    Named array with the calibration points. Must have fields "X" and
    "wavelength(Angs)"

    wave_solution: np.Polynomial
    Wavelength solution
    """
    def __init__(self, calibration_points):
        """Initialize class instance

        Arguments
        ---------
        calibration_points: np.ndarray
        Named array with the calibration points. Must have fields "x" and
        "wave"
        """
        self.calibration_points = calibration_points
        if self.calibration_points.size < MIN_CALIBRATION_POINTS:
            raise CalibrationError(
                "Compute Calibration: Error: too few points")

        # compute the wavelength solution
        self.wave_solution = np.polynomial.Polynomial.fit(
            calibration_points["x"],
            calibration_points["wave"],
            3)

    def calibrate(self, size):
        """Return the wavelength solution

        Arguments
        ---------
        size: int
        Size of the spectrum array
        """
        return self.wave_solution(np.arange(size))

    @classmethod
    def from_file(cls, filename):
        """Compute the wavelength solution from read data points and store it as
        a class intance

        Arguments
        ---------
        filename: str
        Name of the file containing the calibration points

        Return
        ------
        instance: Calibration
        The initialized instance
        """
        calibration_points = np.genfromtxt(filename, names=True)

        return cls(calibration_points)

    @classmethod
    def from_points(cls, calibration_points_dict):
        """Compute the wavelength solution from a dictionary of data points and
        store it as a class intance

        Arguments
        ---------
        calibrationPoints: dict
        Dictionary with the calibration points. Keys are the position in pixels and
        values are the wavelengths

        Return
        ------
        instance: Calibration
        The initialized instance
        """
        calibration_points = np.array(
            list(calibration_points_dict.items()),
            dtype=[("x", float), ("wave", float)]
        )

        return cls(calibration_points)

    def save(self, filename):
        """Save calibration points

        Raise
        -----
        CalibrationError if the filename does not have the correct format
        """
        # check filename extension
        extension = None
        for format_check in ACCEPTED_FORMATS:
            if filename.endswith(format_check):
                extension = format_check
        if extension is None:
            raise CalibrationError(
                "Calibration: 'filename' has incorrect extension. Valid"
                "extensions are " + ", ".join(ACCEPTED_FORMATS)
                )

        with open(filename, "w", encoding="UTF-8") as file:
            file.write("# x wave\n")
            for item in self.calibration_points:
                file.write(f"{item['x']} {item['wave']}\n")
