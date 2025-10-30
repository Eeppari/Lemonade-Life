class Error:
    def __init__(self):
        pass

    def print_error_code(self):
        pass

class SomeError(Error):
    def print_error_code(self):
        print(1)

errorCodes = {
    1 : SomeError
}

def raiseCustomError(errorCode: int):
    if errorCode in errorCodes:
        errorCodes[errorCode].print_error_code()