class PyLGTVPairException(Exception):
    def __init__(self, message):
        self.message = message


class PyLGTVCmdException(Exception):
    def __init__(self, message):
        self.message = message


class PyLGTVCmdError(PyLGTVCmdException):
    def __init__(self, message):
        self.message = message


class PyLGTVServiceNotFoundError(PyLGTVCmdError):
    def __init__(self, message):
        self.message = message

