import os
import gnureadline
import glob

from spectrum import Spectrum
from errors.spectrum_error import SpectrumError

# this is so that raw_input can autocomplete with
def complete(text, state):
    return (glob.glob(text+'*')+[None])[state]

gnureadline.set_completer_delims(' \t\n;')
gnureadline.parse_and_bind("tab: complete")
gnureadline.set_completer(complete)

def loadImage():
    image_name = raw_input("Enter image/spectrum name --> ")
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
        print "###################################"
        print "#        Welcome to PySpec        #"
        print "#                                 #"
        print "# Choose an option:               #"
        print "#   1: (Re)Load image/spectrum    #"
        print "#   2: Extract spectrum           #"
        print "#   3: Plot raw spectrum          #"
        print "#   4: Set calibration            #"
        print "#   5: Calibrate                  #"
        print "#   6: Plot calibrated spectrum   #"
        print "#                                 #"
        print "#   0: End                        #"
        print "#                                 #"
        print "###################################"

        # read chosen option
        try:
            option = int(raw_input("{} --> ".format(message)))
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
            except (AttributeError, NameError):
                message = "Load spectrum first"

        # plot raw spectrum
        elif option == 3:
            mesage = spec.plotRawSpectrum()
                
        # set calibration
        elif option == 4:
            message = "not implemented"
        
        # calibrate
        elif option == 5:
            message = "not implemented"

        # plot calibrated spectrum
        elif option == 6:
            message = spec.plotCalibratedSpectrum()

        # other options
        else:
            status = "main"
