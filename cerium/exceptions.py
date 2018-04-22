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


class CharactersException(AndroidDriverException):
    """
    Thrown when no devices are connected.
    """
    pass

class ParametersException(AndroidDriverException):
    """
    Thrown when a parameter error occurs.
    """
    pass

class PackageException(AndroidDriverException):
    """
    Thrown when the package does not exist.
    """
    pass

class WLANConnectException(AndroidDriverException):
    """
    Thrown when the device is not connected to WLAN.
    """
    pass

class RootPermissionsException(AndroidDriverException):
    """
    Thrown when no root permissions.
    """
    pass

class ApplicationsException(AndroidDriverException):
    """
    Thrown when using the wrong command to run the application.
    """
    pass