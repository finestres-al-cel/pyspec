from spectrum_error import SpectrumError

class SpectrumFormatError(SpectrumError):
    """
        Exception raised when the format of the image filename passed to Spectrum is not
        supported
    """
    def __init__(self, method, message):
        """
            Initialize class instance
            
            METHOD: SpectrumFormatError.__init__
            TYPE: Constructor, public
            
            PURPOSE:
            Initialize class instance
            
            ARGUMENTS:
            method (string):           Name of the mehtod of Spectrum that produced the error
            message (string):          The error message
            
            RETURNS:
            NONE
            
            EXAMPLES:
            * raise SpectrumFormatError(aMethod, "An error message")
            """
        self._method = method
        self._message = message

if __name__ == '__main__':
    raise SpectrumFormatError()

