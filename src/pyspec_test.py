import os
import gnureadline
import glob
from builtins import input
import numpy as np

from spectrum import Spectrum
from errors.spectrum_error import SpectrumError


# this is so that input can autocomplete using the tab
def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

gnureadline.set_completer_delims(' \t\n;')
gnureadline.parse_and_bind("tab: complete")
gnureadline.set_completer(complete)

def loadTestImage():
    image_name = "test/test_image.fits"
    try:
        spec = Spectrum(image_name)
    except SpectrumError as e:
        message = "{}\nLoad error".format(e)
        return message, None

    return "Load successful", spec

def loadRawSpectrum():
    message, spec = loadTestImage()
    if spec is None:
        return message, None
    extracted_spectrum = np.genfromtxt("test/test_image_extracted.dat")
    try:
        spec.setExtractedSpectrum(extracted_spectrum)
    except SpectrumError as e:
        message = "{}\nLoad error".format(e)
        return message, None

    return "Load successful", spec

def loadRawCalibrationSpectrum():
    image_name = "test/test_image_cal.fits"
    try:
        spec = Spectrum(image_name)
    except SpectrumError as e:
        message = "{}\nLoad error".format(e)
        return message, None

    if spec is None:
        return message, None
    extracted_spectrum = np.genfromtxt("test/test_image_cal_extracted.dat", names=True)
    try:
        spec.setExtractedSpectrum(extracted_spectrum["spectrum"])
    except SpectrumError as e:
        message = "{}\nLoad error".format(e)
        return message, None

    return "Load successful", spec


def loadImage():
    image_name = input("Enter image name --> ")
    try:
        spec = Spectrum(image_name)
    except SpectrumError as e:
        message = "{}\nLoad error".format(e)
        return message, None

    return "Load successful", spec


if __name__ == "__main__":


    status = "main"
    message = ""
    while status != "end":
        os.system('clear')
        option = -1
        print("###################################")
        print("#        Welcome to PySpec        #")
        print("#        test mode enabled        #")
        print("#                                 #")
        print("# Choose an option:               #")
        print("#   1: (Re)Load image             #")
        print("#   2: Extract spectrum           #")
        print("#   3: Plot raw spectrum          #")
        print("#   4: Set calibration            #")
        print("#   5: Load calibration           #")
        print("#   6: Plot calibrated spectrum   #")
        print("#                                 #")
        print("#   0: End                        #")
        print("#                                 #")
        print("###################################")

        # read chosen option
        try:
            option = int(input("{} --> ".format(message)))
            meassage = ""
        except ValueError:
            message = ""

        # end program
        if option == 0:
            status = "end"

        # load spectrum image
        elif option == 1:
            message, spec = loadImage()

        # extract spectrum
        elif option == 2:
            try:
                message = spec.extract()
            except (AttributeError, NameError) as e:
                message, spec = loadTestImage()
                try:
                    message = spec.extract()
                except (AttributeError, NameError) as e:
                    print(e)
                    message = "Load spectrum first"

        # plot raw spectrum
        elif option == 3:
            try:
                message = spec.plotRawSpectrum()
            except (AttributeError, NameError) as e:
                try:
                    message, spec = loadRawSpectrum()
                    message = spec.plotRawSpectrum()
                except (AttributeError, NameError) as e:
                    print(e)
                    message = "Extract spectrum first"

        # set calibration
        elif option == 4:
            try:
                message = spec.setCalibration()
            except (AttributeError, NameError) as e:
                try:
                    message, spec = loadRawCalibrationSpectrum()
                    message = spec.setCalibration()
                except (AttributeError, NameError) as e:
                    print(e)
                    message = "Extract spectrum first"

        # calibrate
        elif option == 5:
            try:
                message = spec.loadCalibration()
            except (AttributeError, NameError) as e:
                try:
                    message, spec = loadRawCalibrationSpectrum()
                    message = spec.loadCalibration()
                except (AttributeError, NameError) as e:
                    print(e)
                    message = "Extract spectrum first"

        # plot calibrated spectrum
        elif option == 6:
            message = spec.plotCalibratedSpectrum()

        # other options
        else:
            status = "main"
