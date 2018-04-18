"""
Exceptions that may happen in all the androiddriver code.

"""


class AndroidDriverException(Exception):
    """
    Base androiddriver exception.
    """
    def __init__(self, msg=None):
        self.msg = msg

    def __str__(self):
        return self.msg


class InvalidPATHException(AndroidDriverException):
    """
    Thrown when the adb PATH doesn't exist.
    """
    pass


class DeviceConnectionException(AndroidDriverException):
    """
    Thrown when no devices are connected.
    """
    pass