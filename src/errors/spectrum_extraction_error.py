from spectrum_error import SpectrumError

class SpectrumExtractionError(SpectrumError):
    """
        Exception raised when the extraction of a Spectrum fails
    """
    def __init__(self, method, message):
        """
            Initialize class instance
            
            METHOD: SpectrumExtractionError.__init__
            TYPE: Constructor, public
            
            PURPOSE:
            Initialize class instance
            
            ARGUMENTS:
            method (string):           Name of the mehtod of Spectrum that produced the error
            message (string):          The error message
            
            RETURNS:
            NONE
            
            EXAMPLES:
            * raise SpectrumExtractionError(aMethod, "An error message")
            """
        self._method = method
        self._message = message

if __name__ == '__main__':
    raise SpectrumExtractionError()

