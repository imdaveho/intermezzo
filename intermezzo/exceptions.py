from __future__ import unicode_literals


class ResizeScreenError(Exception):
    """
    Asciimatics raises this Exception if the terminal is resized while playing
    a Scene (and the Screen has been told not to ignore a resizing event).
    """

    def __init__(self, message, scene=None):
        """
        :param message: Error message for this exception.
        :param scene: Scene that was active at time of resize.
        """
        super(ResizeScreenError, self).__init__()
        self._scene = scene
        self._message = message

    def __str__(self):
        """
        Printable form of the exception.
        """
        return self._message

    @property
    def scene(self):
        """
        The Scene that was running when the Screen resized.
        """
        return self._scene


class StopApplication(Exception):
    """
    Any component can raise this exception to tell Asciimatics to stop running.
    If playing a Scene (i.e. inside `Screen.play()`) the Screen will return
    to the calling function.  When used at any other time, the exception will
    need to be caught by the application using Asciimatics.
    """

    def __init__(self, message):
        """
        :param message: Error message for this exception.
        """
        super(StopApplication, self).__init__()
        self._message = message

    def __str__(self):
        """
        Printable form of the exception.
        """
        return self._message
