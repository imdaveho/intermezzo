# -*- coding: utf-8 -*-
from __future__ import division
from __future__ import absolute_import
from __future__ import print_function
from __future__ import unicode_literals
import struct
from builtins import object
from builtins import range
from builtins import str
from builtins import ord
from builtins import chr
from future.utils import with_metaclass
from abc import ABCMeta, abstractmethod
import json
import sys
import signal

from intermezzo.terminal.event import KeyboardEvent, MouseEvent
from intermezzo.terminal.exceptions import ResizeScreenError, StopApplication
from intermezzo.terminal import constants as cnst


class _AbstractCanvas(with_metaclass(ABCMeta, object)):
    """
    Abstract class to handle screen buffering.
    """

    def __init__(self, height, width, buffer_height, colours, unicode_aware):
        """
        :param height: The buffer height for this object.
        :param width: The buffer width for this object.
        :param buffer_height: The buffer height for this object.
        :param colours: Number of colours for this object.
        :param unicode_aware: Force use of unicode options for this object.
        """
        super(_AbstractCanvas, self).__init__()

        # Can we handle unicode environments?
        self._unicode_aware = unicode_aware

        # Create screen buffers.
        self.height = height
        self.width = width
        self.colours = colours
        self._buffer_height = buffer_height
        self._screen_buffer = None
        self._double_buffer = None
        self._start_line = 0
        self._x = 0
        self._y = 0

        # Reset the screen ready to go...
        self.reset()

    def reset(self):
        """
        Reset the internal buffers for the abstract canvas.
        """
        # Reset our screen buffer
        self._start_line = 0
        self._x = self._y = None
        line = [(u" ", cnst.COLOUR_WHITE, 0, 0) for _ in range(self.width)]
        # Note that we use json to duplicate the data as copy.deepcopy is an
        # order of magnitude slower.
        self._screen_buffer = [
            json.loads(json.dumps(line)) for _ in range(self._buffer_height)]
        self._double_buffer = json.loads(json.dumps(self._screen_buffer))
        self._reset()

    def scroll(self):
        """
        Scroll the abstract canvas up one line.
        """
        self._start_line += 1

    def scroll_to(self, line):
        """
        Scroll the abstract canvas to make a specific line.

        :param line: The line to scroll to.
        """
        self._start_line = line

    @abstractmethod
    def _reset(self):
        """
        Internal implementation required to reset underlying drawing
        interface.
        """

    @abstractmethod
    def refresh(self):
        """
        Refresh this object - this will draw to the underlying display
        interface.
        """

    def get_from(self, x, y):
        """
        Get the character at the specified location.

        :param x: The column (x coord) of the character.
        :param y: The row (y coord) of the character.

        :return: A 4-tuple of (ascii code, foreground, attributes, background)
                 for the character at the location.
        """
        if y < 0 or y >= self._buffer_height or x < 0 or x >= self.width:
            return None
        cell = self._double_buffer[y][x]
        return ord(cell[0]), cell[1], cell[2], cell[3]

    def print_at(self, text, x, y, colour=7, attr=0, bg=0, transparent=False):
        """
        Print the text at the specified location using the
        specified colour and attributes.

        :param text: The (single line) text to be printed.
        :param x: The column (x coord) for the start of the text.
        :param y: The line (y coord) for the start of the text.
        :param colour: The colour of the text to be displayed.
        :param attr: The cell attribute of the text to be displayed.
        :param bg: The background colour of the text to be displayed.
        :param transparent: Whether to print spaces or not, thus giving a
            transparent effect.

        The colours and attributes are the COLOUR_xxx and A_yyy constants
        defined in the Screen class.
        """
        # Trim text to the buffer.
        if y < 0 or y >= self._buffer_height or x > self.width:
            return
        if x < 0:
            text = text[-x:]
            x = 0
        if x + len(text) >= self.width:
            text = text[:self.width - x]

        if len(text) > 0:
            for i, c in enumerate(text):
                if c != " " or not transparent:
                    self._double_buffer[y][x + i] = (str(c), colour, attr, bg)

    @property
    def start_line(self):
        """
        :return: The start line of the top of the canvas.
        """
        return self._start_line

    @property
    def unicode_aware(self):
        """
        :return: Whether unicode input/output is supported or not.
        """
        return self._unicode_aware

    @property
    def dimensions(self):
        """
        :return: The full dimensions of the canvas as a (height, width) tuple.
        """
        return self.height, self.width

    def centre(self, text, y, colour=7, attr=0, colour_map=None):
        """
        Centre the text on the specified line (y) using the optional
        colour and attributes.

        :param text: The (single line) text to be printed.
        :param y: The line (y coord) for the start of the text.
        :param colour: The colour of the text to be displayed.
        :param attr: The cell attribute of the text to be displayed.
        :param colour_map: Colour/attribute list for multi-colour text.

        The colours and attributes are the COLOUR_xxx and A_yyy constants
        defined in the Screen class.
        """
        x = (self.width - len(text)) // 2
        self.paint(text, x, y, colour, attr, colour_map=colour_map)

    def paint(self, text, x, y, colour=7, attr=0, bg=0, transparent=False,
              colour_map=None):
        """
        Paint multi-colour text at the defined location.

        :param text: The (single line) text to be printed.
        :param x: The column (x coord) for the start of the text.
        :param y: The line (y coord) for the start of the text.
        :param colour: The default colour of the text to be displayed.
        :param attr: The default cell attribute of the text to be displayed.
        :param bg: The default background colour of the text to be displayed.
        :param transparent: Whether to print spaces or not, thus giving a
            transparent effect.
        :param colour_map: Colour/attribute list for multi-colour text.

        The colours and attributes are the COLOUR_xxx and A_yyy constants
        defined in the Screen class.
        colour_map is a list of tuples (foreground, attribute, background) that
        must be the same length as the passed in text (or None if no mapping is
        required).
        """
        if colour_map is None:
            self.print_at(text, x, y, colour, attr, bg, transparent)
        else:
            for i, c in enumerate(text):
                if len(colour_map[i]) > 0 and colour_map[i][0] is not None:
                    colour = colour_map[i][0]
                if len(colour_map[i]) > 1 and colour_map[i][1] is not None:
                    attr = colour_map[i][1]
                if len(colour_map[i]) > 2 and colour_map[i][2] is not None:
                    bg = colour_map[i][2]
                self.print_at(c, x + i, y, colour, attr, bg, transparent)

    def is_visible(self, x, y):
        """
        Return whether the specified location is on the visible screen.

        :param x: The column (x coord) for the location to check.
        :param y: The line (y coord) for the location to check.
        """
        return ((x >= 0) and
                (x <= self.width) and
                (y >= self._start_line) and
                (y < self._start_line + self.height))

    def move(self, x, y):
        """
        Move the drawing cursor to the specified position.

        :param x: The column (x coord) for the location to check.
        :param y: The line (y coord) for the location to check.
        """
        self._x = int(round(x, 1)) * 2
        self._y = int(round(y, 1)) * 2


class Canvas(_AbstractCanvas):
    """
    A Canvas is an object that can be used to draw to the screen. It maintains
    its own buffer that will be flushed to the screen when `refresh()` is
    called.
    """

    def __init__(self, screen, height, width, x=None, y=None):
        """
        :param screen: The underlying Screen that will be drawn to on refresh.
        :param height: The height of the screen buffer to be used.
        :param width: The width of the screen buffer to be used.
        :param x: The x position for the top left corner of the Canvas.
        :param y: The y position for the top left corner of the Canvas.

        If either of the x or y positions is not set, the Canvas will default
        to centring within the current Screen for that location.
        """
        # Save off the screen details.
        # TODO: Fix up buffer logic once and for all!
        super(Canvas, self).__init__(
            height, width, 200, screen.colours, screen.unicode_aware)
        self._screen = screen
        self._dx = (screen.width - width) // 2 if x is None else x
        self._dy = (screen.height - height) // 2 if y is None else y

    def refresh(self):
        """
        Flush the canvas content to the underlying screen.
        """
        for y in range(self.height):
            for x in range(self.width):
                c = self._double_buffer[y + self._start_line][x]
                self._screen.print_at(
                    c[0], x + self._dx, y + self._dy, c[1], c[2], c[3])

    def _reset(self):
        # Nothing needed for a Canvas
        pass

    @property
    def origin(self):
        """
        The location of top left corner of the canvas on the Screen.

        :returns: A tuple (x, y) of the location
        """
        return self._dx, self._dy


class Screen(with_metaclass(ABCMeta, _AbstractCanvas)):
    """
    Class to track basic state of the screen.

    This is an abstract class that will build the correct concrete class for
    you when you call :py:meth:`.wrapper`.  If needed, you can use the
    :py:meth:`~.Screen.open` and :py:meth:`~.Screen.close` methods for finer
    grained control of the construction and tidy up.

    Note that you need to define the required height for your screen buffer.
    This is important if you plan on handling the scrolling of the screen.
    It must be big enough to handle the full range of scrolling.
    """

    def __init__(self, height, width, buffer_height, unicode_aware):
        """
        Don't call this constructor directly.
        """
        super(Screen, self).__init__(
            height, width, buffer_height, 0, unicode_aware)

        # Initialize base class variables - e.g. those used for drawing.
        self.height = height
        self.width = width
        self._last_start_line = 0

        # Set up internal state for colours - used by children to determine
        # changes to text colour when refreshing the screen.
        self._colour = 0
        self._attr = 0
        self._bg = 0

        # tracking of current cursor position - used in screen refresh.
        self._cur_x = 0
        self._cur_y = 0

        # Control variables for playing out a set of Scenes.
        self._scenes = []
        self._scene_index = 0
        self._frame = 0
        self._idle_frame_count = 0
        self._unhandled_input = self._unhandled_event_default

    @classmethod
    def open(cls, height=200, catch_interrupt=False, unicode_aware=None):
        """
        Construct a new Screen for any platform.  This will just create the
        correct Screen object for your environment.  See :py:meth:`.wrapper` for
        a function to create and tidy up once you've finished with the Screen.

        :param height: The buffer height for this window (if using scrolling).
        :param catch_interrupt: Whether to catch and prevent keyboard
            interrupts.  Defaults to False to maintain backwards compatibility.
        :param unicode_aware: Whether the application can use unicode or not.
            If None, try to detect from the environment if UTF-8 is enabled.
        """
        if sys.platform == "win32":
            screen = win32.open(cls, height, catch_interrupt, unicode_aware)
        else:
            screen = unix.open(cls, height, catch_interrupt, unicode_aware)
        return screen

    @abstractmethod
    def close(self, restore=True):
        """
        Close down this Screen and tidy up the environment as required.

        :param restore: whether to restore the environment or not.
        """

    @classmethod
    def wrapper(cls, func, height=200, catch_interrupt=False, arguments=None,
                unicode_aware=None):
        """
        Construct a new Screen for any platform.  This will initialize the
        Screen, call the specified function and then tidy up the system as
        required when the function exits.

        :param func: The function to call once the Screen has been created.
        :param height: The buffer height for this Screen (if using scrolling).
        :param catch_interrupt: Whether to catch and prevent keyboard
            interrupts.  Defaults to False to maintain backwards compatibility.
        :param arguments: Optional arguments list to pass to func (after the
            Screen object).
        :param unicode_aware: Whether the application can use unicode or not.
            If None, try to detect from the environment if UTF-8 is enabled.
        """
        screen = Screen.open(height,
                             catch_interrupt=catch_interrupt,
                             unicode_aware=unicode_aware)
        restore = True
        try:
            try:
                if arguments:
                    func(screen, *arguments)
                else:
                    func(screen)
            except ResizeScreenError:
                restore = False
                raise
        finally:
            screen.close(restore)

    def _reset(self):
        """
        Reset the Screen.
        """
        self._last_start_line = 0
        self._colour = None
        self._attr = None
        self._bg = None
        self._cur_x = None
        self._cur_y = None

    def refresh(self):
        """
        Refresh the screen.
        """
        # Scroll the screen as required to minimize redrawing.
        if self._last_start_line != self._start_line:
            self._scroll(self._start_line - self._last_start_line)
            self._last_start_line = self._start_line

        # Now draw any deltas to the scrolled screen.
        for y in range(min(self.height, self._buffer_height)):
            for x in range(self.width):
                new_cell = self._double_buffer[y + self._start_line][x]
                if self._screen_buffer[y + self._start_line][x] != new_cell:
                    self._change_colours(new_cell[1], new_cell[2], new_cell[3])
                    self._print_at(new_cell[0], x, y)
                    self._screen_buffer[y + self._start_line][x] = new_cell

    def clear(self):
        """
        Clear the Screen of all content.
        """
        # Clear the actual terminal
        self.reset()
        self._change_colours(cnst.COLOUR_WHITE, 0, 0)
        self._clear()

    def get_key(self):
        """
        Check for a key without waiting.  This method is deprecated.  Use
        :py:meth:`.get_event` instead.
        """
        event = self.get_event()
        if event and isinstance(event, KeyboardEvent):
            return event.key_code
        return None

    @abstractmethod
    def get_event(self):
        """
        Check for any events (e.g. key-press or mouse movement) without waiting.

        :returns: A :py:obj:`.Event` object if anything was detected, otherwise
                  it returns None.
        """

    @abstractmethod
    def has_resized(self):
        """
        Check whether the screen has been re-sized.

        :returns: True when the screen has been re-sized since the last check.
        """

    @staticmethod
    def _unhandled_event_default(event):
        """
        Default unhandled event handler for handling simple scene navigation.
        """
        if isinstance(event, KeyboardEvent):
            c = event.key_code
            if c in (ord("X"), ord("x"), ord("Q"), ord("q")):
                raise StopApplication("User terminated app")

    @abstractmethod
    def _change_colours(self, colour, attr, bg):
        """
        Change current colour if required.

        :param colour: New colour to use.
        :param attr: New attributes to use.
        :param bg: New background colour to use.
        """

    @abstractmethod
    def _print_at(self, text, x, y):
        """
        Print string at the required location.

        :param text: The text string to print.
        :param x: The x coordinate
        :param y: The Y coordinate
        """

    @abstractmethod
    def _clear(self):
        """
        Clear the window.
        """

    @abstractmethod
    def _scroll(self, lines):
        """
        Scroll the window up or down.

        :param lines: Number of lines to scroll.  Negative numbers scroll down.
        """

    @abstractmethod
    def set_title(self, title):
        """
        Set the title for this terminal/console session.  This will typically
        change the text displayed in the window title bar.

        :param title: The title to be set.
        """

if sys.platform in ('win32',):
    from intermezzo.terminal.platform import win32
elif sys.platform in ('linux', 'darwin'):
    from intermezzo.terminal.platform import unix
