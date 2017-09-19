from spectrum_error import SpectrumError

class SpectrumFileError(SpectrumError):
    """
        Exception raised when attempting to read a file and the file is not existent
    """
    def __init__(self, method, message):
        """
            Initialize class instance
            
            METHOD: SpectrumFileError.__init__
            TYPE: Constructor, public
            
            PURPOSE:
            Initialize class instance
            
            ARGUMENTS:
            method (string):           Name of the mehtod of Spectrum that produced the error
            message (string):          The error message
            
            RETURNS:
            NONE
            
            EXAMPLES:
            * raise SpectrumFileError(aMethod, "An error message")
            """
        self._method = method
        self._message = message

if __name__ == '__main__':
    raise SpectrumFileError()

