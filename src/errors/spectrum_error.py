from errors.error import Error

class SpectrumError(Error):
    """
        The base class for all exceptions related to Spectrum class
    """
    def __str__(self):
        """
            Returns a printable representation of the error message

            FUNCTION: SpectrumError.__str__
            TYPE: Public
            PURPOSE: Returns a printable representation of the error message
            RETURNS:
            A printable representation of the error message
            EXAMPLES:
            print SpectrumError("this is a warning")
            """
        return 'In method Spectrum.{method}: {message}'.format(method=self._method, message=repr(self._message))

if __name__ == '__main__':
    pass
