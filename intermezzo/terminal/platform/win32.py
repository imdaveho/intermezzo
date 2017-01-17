import time
from intermezzo.terminal.screen import Screen
from intermezzo.terminal import constants as cnst
from intermezzo.terminal.event import KeyboardEvent, MouseEvent

# Logging
from logging import getLogger
logger = getLogger(__name__)

import win32console
import win32con
import pywintypes
import win32file
from win32console import STD_OUTPUT_HANDLE, STD_INPUT_HANDLE
from win32file import GENERIC_READ, FILE_SHARE_READ, OPEN_ALWAYS, \
    GENERIC_WRITE, FILE_SHARE_WRITE

# Make sure to install PyWin32 as a set
# of useful Windows-specific Python modules

# Looks like pywin32 is missing some Windows constants
ENABLE_EXTENDED_FLAGS = 0x0080
ENABLE_QUICK_EDIT_MODE = 0x0040

def open(cls, height=200, catch_interrupt=False, unicode_aware=None):
    # Clone the standard output buffer so that we can do whatever we
    # need for the application, but restore the buffer at the end.
    # Note that we need to resize the clone to ensure that it is the
    # same size as the original in some versions of Windows.
    old_out = win32console.PyConsoleScreenBufferType(
        win32file.CreateFile("CONOUT$",
                             GENERIC_READ | GENERIC_WRITE,
                             FILE_SHARE_WRITE,
                             None,
                             OPEN_ALWAYS,
                             0,
                             None))
    try:
        info = old_out.GetConsoleScreenBufferInfo()
    except pywintypes.error:
        info = None
    win_out = win32console.CreateConsoleScreenBuffer()
    if info:
        win_out.SetConsoleScreenBufferSize(info['Size'])
    else:
        win_out.SetStdHandle(STD_OUTPUT_HANDLE)
    win_out.SetConsoleActiveScreenBuffer()

    # Get the standard input buffer.
    win_in = win32console.PyConsoleScreenBufferType(
        win32file.CreateFile("CONIN$",
                             GENERIC_READ | GENERIC_WRITE,
                             FILE_SHARE_READ,
                             None,
                             OPEN_ALWAYS,
                             0,
                             None))
    win_in.SetStdHandle(STD_INPUT_HANDLE)

    # Hide the cursor.
    # win_out.SetConsoleCursorInfo(1, 0)

    # Disable scrolling
    out_mode = win_out.GetConsoleMode()
    win_out.SetConsoleMode(
        out_mode & ~ win32console.ENABLE_WRAP_AT_EOL_OUTPUT)

    # Enable mouse input, disable quick-edit mode and disable ctrl-c
    # if needed.
    in_mode = win_in.GetConsoleMode()
    new_mode = (in_mode | win32console.ENABLE_MOUSE_INPUT |
                ENABLE_EXTENDED_FLAGS)
    new_mode &= ~ENABLE_QUICK_EDIT_MODE
    if catch_interrupt:
        # Ignore ctrl-c handlers if specified.
        new_mode &= ~win32console.ENABLE_PROCESSED_INPUT
    win_in.SetConsoleMode(new_mode)

    screen = _WindowsScreen(win_out, win_in, height, old_out, in_mode,
                            unicode_aware=unicode_aware)
    return screen

class _WindowsScreen(Screen):
    """
    Windows screen implementation.
    """

    # Virtual key code mapping.
    _KEY_MAP = {
        win32con.VK_ESCAPE: cnst.KEY_ESCAPE,
        win32con.VK_F1: cnst.KEY_F1,
        win32con.VK_F2: cnst.KEY_F2,
        win32con.VK_F3: cnst.KEY_F3,
        win32con.VK_F4: cnst.KEY_F4,
        win32con.VK_F5: cnst.KEY_F5,
        win32con.VK_F6: cnst.KEY_F6,
        win32con.VK_F7: cnst.KEY_F7,
        win32con.VK_F8: cnst.KEY_F8,
        win32con.VK_F9: cnst.KEY_F9,
        win32con.VK_F10: cnst.KEY_F10,
        win32con.VK_F11: cnst.KEY_F11,
        win32con.VK_F12: cnst.KEY_F12,
        win32con.VK_F13: cnst.KEY_F13,
        win32con.VK_F14: cnst.KEY_F14,
        win32con.VK_F15: cnst.KEY_F15,
        win32con.VK_F16: cnst.KEY_F16,
        win32con.VK_F17: cnst.KEY_F17,
        win32con.VK_F18: cnst.KEY_F18,
        win32con.VK_F19: cnst.KEY_F19,
        win32con.VK_F20: cnst.KEY_F20,
        win32con.VK_F21: cnst.KEY_F21,
        win32con.VK_F22: cnst.KEY_F22,
        win32con.VK_F23: cnst.KEY_F23,
        win32con.VK_F24: cnst.KEY_F24,
        win32con.VK_PRINT: cnst.KEY_PRINT_SCREEN,
        win32con.VK_INSERT: cnst.KEY_INSERT,
        win32con.VK_DELETE: cnst.KEY_DELETE,
        win32con.VK_HOME: cnst.KEY_HOME,
        win32con.VK_END: cnst.KEY_END,
        win32con.VK_LEFT: cnst.KEY_LEFT,
        win32con.VK_UP: cnst.KEY_UP,
        win32con.VK_RIGHT: cnst.KEY_RIGHT,
        win32con.VK_DOWN: cnst.KEY_DOWN,
        win32con.VK_PRIOR: cnst.KEY_PAGE_UP,
        win32con.VK_NEXT: cnst.KEY_PAGE_DOWN,
        win32con.VK_BACK: cnst.KEY_BACK,
        win32con.VK_TAB: cnst.KEY_TAB,
    }

    _EXTRA_KEY_MAP = {
        win32con.VK_NUMPAD0: cnst.KEY_NUMPAD0,
        win32con.VK_NUMPAD1: cnst.KEY_NUMPAD1,
        win32con.VK_NUMPAD2: cnst.KEY_NUMPAD2,
        win32con.VK_NUMPAD3: cnst.KEY_NUMPAD3,
        win32con.VK_NUMPAD4: cnst.KEY_NUMPAD4,
        win32con.VK_NUMPAD5: cnst.KEY_NUMPAD5,
        win32con.VK_NUMPAD6: cnst.KEY_NUMPAD6,
        win32con.VK_NUMPAD7: cnst.KEY_NUMPAD7,
        win32con.VK_NUMPAD8: cnst.KEY_NUMPAD8,
        win32con.VK_NUMPAD9: cnst.KEY_NUMPAD9,
        win32con.VK_MULTIPLY: cnst.KEY_MULTIPLY,
        win32con.VK_ADD: cnst.KEY_ADD,
        win32con.VK_SUBTRACT: cnst.KEY_SUBTRACT,
        win32con.VK_DECIMAL: cnst.KEY_DECIMAL,
        win32con.VK_DIVIDE: cnst.KEY_DIVIDE,
        win32con.VK_CAPITAL: cnst.KEY_CAPS_LOCK,
        win32con.VK_NUMLOCK: cnst.KEY_NUM_LOCK,
        win32con.VK_SCROLL: cnst.KEY_SCROLL_LOCK,
        win32con.VK_SHIFT: cnst.KEY_SHIFT,
        win32con.VK_CONTROL: cnst.KEY_CONTROL,
        win32con.VK_MENU: cnst.KEY_MENU,
    }

    # Foreground colour lookup table.
    _COLOURS = {
        cnst.COLOUR_BLACK: 0,
        cnst.COLOUR_RED: win32console.FOREGROUND_RED,
        cnst.COLOUR_GREEN: win32console.FOREGROUND_GREEN,
        cnst.COLOUR_YELLOW: (win32console.FOREGROUND_RED |
                               win32console.FOREGROUND_GREEN),
        cnst.COLOUR_BLUE: win32console.FOREGROUND_BLUE,
        cnst.COLOUR_MAGENTA: (win32console.FOREGROUND_RED |
                                win32console.FOREGROUND_BLUE),
        cnst.COLOUR_CYAN: (win32console.FOREGROUND_BLUE |
                             win32console.FOREGROUND_GREEN),
        cnst.COLOUR_WHITE: (win32console.FOREGROUND_RED |
                              win32console.FOREGROUND_GREEN |
                              win32console.FOREGROUND_BLUE)
    }

    # Background colour lookup table.
    _BG_COLOURS = {
        cnst.COLOUR_BLACK: 0,
        cnst.COLOUR_RED: win32console.BACKGROUND_RED,
        cnst.COLOUR_GREEN: win32console.BACKGROUND_GREEN,
        cnst.COLOUR_YELLOW: (win32console.BACKGROUND_RED |
                               win32console.BACKGROUND_GREEN),
        cnst.COLOUR_BLUE: win32console.BACKGROUND_BLUE,
        cnst.COLOUR_MAGENTA: (win32console.BACKGROUND_RED |
                                win32console.BACKGROUND_BLUE),
        cnst.COLOUR_CYAN: (win32console.BACKGROUND_BLUE |
                             win32console.BACKGROUND_GREEN),
        cnst.COLOUR_WHITE: (win32console.BACKGROUND_RED |
                              win32console.BACKGROUND_GREEN |
                              win32console.BACKGROUND_BLUE)
    }

    # Attribute lookup table
    _ATTRIBUTES = {
        0: lambda x: x,
        cnst.A_BOLD: lambda x: x | win32console.FOREGROUND_INTENSITY,
        cnst.A_NORMAL: lambda x: x,
        # Windows console uses a bitmap where background is the top nibble,
        # so we can reverse by swapping nibbles.
        cnst.A_REVERSE: lambda x: ((x & 15) * 16) + ((x & 240) // 16),
        cnst.A_UNDERLINE: lambda x: x
    }

    def __init__(self, stdout, stdin, buffer_height, old_out, old_in,
                 unicode_aware=False):
        """
        :param stdout: The win32console PyConsoleScreenBufferType object for
            stdout.
        :param stdin: The win32console PyConsoleScreenBufferType object for
            stdin.
        :param buffer_height: The buffer height for this window (if using
            scrolling).
        :param old_out: The original win32console PyConsoleScreenBufferType
            object for stdout that should be restored on exit.
        :param old_in: The original stdin state that should be restored on
            exit.
        :param unicode_aware: Whether this Screen can use unicode or not.
        """
        # Save off the screen details and set up the scrolling pad.
        info = stdout.GetConsoleScreenBufferInfo()['Window']
        width = info.Right - info.Left + 1
        height = info.Bottom - info.Top + 1

        # Detect UTF-8 if needed and then construct the Screen.
        if unicode_aware is None:
            # According to MSDN, 65001 is the Windows UTF-8 code page.
            unicode_aware = win32console.GetConsoleCP() == 65001
        super(_WindowsScreen, self).__init__(
            height, width, buffer_height, unicode_aware)

        # Save off the console details.
        self._stdout = stdout
        self._stdin = stdin
        self._last_width = width
        self._last_height = height
        self._old_out = old_out
        self._old_in = old_in

        # Windows is limited to the ANSI colour set.
        self.colours = 8

        # Opt for compatibility with Linux by default
        self._map_all = False

        # Set of keys currently pressed.
        self._keys = set()

    def close(self, restore=True):
        """
        Close down this Screen and tidy up the environment as required.

        :param restore: whether to restore the environment or not.
        """
        if restore:
            # Reset the original screen settings.
            self._old_out.SetConsoleActiveScreenBuffer()
            self._stdin.SetConsoleMode(self._old_in)

    def map_all_keys(self, state):
        """
        Switch on extended keyboard mapping for this Screen.

        :param state: Boolean flag where true means map all keys.

        Enabling this setting will allow Windows to tell you when any key
        is pressed, including metakeys (like shift and control) and whether
        the numeric keypad keys have been used.

        .. warning::

            Using this means your application will not be compatible across
            all platforms.
        """
        self._map_all = state

    def get_event(self):
        """
        Check for any event without waiting.
        """
        # Look for a new event and consume it if there is one.
        while len(self._stdin.PeekConsoleInput(1)) > 0:
            event = self._stdin.ReadConsoleInput(1)[0]
            if event.EventType == win32console.KEY_EVENT:
                # Pasting unicode text appears to just generate key-up
                # events (as if you had pressed the Alt keys plus the
                # keypad code for the character), but the rest of the
                # console input simply doesn't
                # work with key up events - e.g. misses keyboard repeats.
                #
                # We therefore allow any key press (i.e. KeyDown) event and
                # _any_ event that appears to have popped up from nowhere
                # as long as the Alt key is present.
                key_code = ord(event.Char)
                logger.debug("Processing key: %x", key_code)
                if (event.KeyDown or
                        (key_code > 0 and key_code not in self._keys and
                         event.VirtualKeyCode == win32con.VK_MENU)):
                    # Record any keys that were pressed.
                    if event.KeyDown:
                        self._keys.add(key_code)

                    # Translate keys into a KeyboardEvent object.
                    if event.VirtualKeyCode in self._KEY_MAP:
                        key_code = self._KEY_MAP[event.VirtualKeyCode]

                    # Sadly, we are limited to Linux terminal input and so
                    # can't return modifier states in a cross-platform way.
                    # If the user decided not to be cross-platform, so be
                    # it, otherwise map some standard bindings for extended
                    # keys.
                    if (self._map_all and
                            event.VirtualKeyCode in self._EXTRA_KEY_MAP):
                        key_code = self._EXTRA_KEY_MAP[event.VirtualKeyCode]
                    else:
                        if (event.VirtualKeyCode == win32con.VK_TAB and
                                event.ControlKeyState &
                                win32con.SHIFT_PRESSED):
                            key_code = Screen.KEY_BACK_TAB

                    # Don't return anything if we didn't have a valid
                    # mapping.
                    if key_code:
                        return KeyboardEvent(key_code)
                else:
                    # Tidy up any key that was previously pressed.  At
                    # start-up, we may be mid-key, so can't assume this must
                    # always match up.
                    if key_code in self._keys:
                        self._keys.remove(key_code)

            elif event.EventType == win32console.MOUSE_EVENT:
                # Translate into a MouseEvent object.
                logger.debug("Processing mouse: %d, %d",
                             event.MousePosition.X, event.MousePosition.Y)
                button = 0
                if event.EventFlags == 0:
                    # Button pressed - translate it.
                    if (event.ButtonState &
                            win32con.FROM_LEFT_1ST_BUTTON_PRESSED != 0):
                        button |= MouseEvent.LEFT_CLICK
                    if (event.ButtonState &
                            win32con.RIGHTMOST_BUTTON_PRESSED != 0):
                        button |= MouseEvent.RIGHT_CLICK
                elif event.EventFlags & win32con.DOUBLE_CLICK != 0:
                    button |= MouseEvent.DOUBLE_CLICK

                return MouseEvent(event.MousePosition.X,
                                  event.MousePosition.Y,
                                  button)

        # If we get here, we've fully processed the event queue and found
        # nothing interesting.
        return None

    def has_resized(self):
        """
        Check whether the screen has been re-sized.
        """
        # Get the current Window dimensions and check them against last
        # time.
        re_sized = False
        info = self._stdout.GetConsoleScreenBufferInfo()['Window']
        width = info.Right - info.Left + 1
        height = info.Bottom - info.Top + 1
        if width != self._last_width or height != self._last_height:
            re_sized = True
        return re_sized

    def _change_colours(self, colour, attr, bg):
        """
        Change current colour if required.

        :param colour: New colour to use.
        :param attr: New attributes to use.
        :param bg: New background colour to use.
        """
        # Change attribute first as this will reset colours when swapping
        # modes.
        if colour != self._colour or attr != self._attr or self._bg != bg:
            new_attr = self._ATTRIBUTES[attr](
                self._COLOURS[colour] + self._BG_COLOURS[bg])
            self._stdout.SetConsoleTextAttribute(new_attr)
            self._attr = attr
            self._colour = colour
            self._bg = bg

    def _print_at(self, text, x, y):
        """
        Print string at the required location.

        :param text: The text string to print.
        :param x: The x coordinate
        :param y: The Y coordinate
        """
        # We can throw temporary errors on resizing, so catch and ignore
        # them on the assumption that we'll resize shortly.
        try:
            # Move the cursor if necessary
            if x != self._cur_x or y != self._cur_y:
                self._stdout.SetConsoleCursorPosition(
                    win32console.PyCOORDType(x, y))

            # Print the text at the required location and update the current
            # position.
            self._stdout.WriteConsole(text)
            self._cur_x = x + len(text)
            self._cur_y = y
        except pywintypes.error:
            pass

    def _scroll(self, lines):
        """
        Scroll the window up or down.

        :param lines: Number of lines to scroll.  Negative numbers scroll
            down.
        """
        # Scroll the visible screen up by one line
        info = self._stdout.GetConsoleScreenBufferInfo()['Window']
        rectangle = win32console.PySMALL_RECTType(
            info.Left, info.Top + lines, info.Right, info.Bottom)
        new_pos = win32console.PyCOORDType(0, info.Top)
        self._stdout.ScrollConsoleScreenBuffer(
            rectangle, None, new_pos, " ", 0)

    def _clear(self):
        """
        Clear the terminal.
        """
        info = self._stdout.GetConsoleScreenBufferInfo()['Window']
        width = info.Right - info.Left + 1
        height = info.Bottom - info.Top + 1
        box_size = width * height
        self._stdout.FillConsoleOutputAttribute(
            0, box_size, win32console.PyCOORDType(0, 0))
        self._stdout.FillConsoleOutputCharacter(
            " ", box_size, win32console.PyCOORDType(0, 0))
        self._stdout.SetConsoleCursorPosition(
            win32console.PyCOORDType(0, 0))

    def set_title(self, title):
        """
        Set the title for this terminal/console session.  This will
        typically change the text displayed in the window title bar.

        :param title: The title to be set.
        """
        win32console.SetConsoleTitle(title)

    # Additions for Impromptu
    # for cursor management
    def _move_cursor(self, x, y):
        """
        Move the default console cursor.
        Copy of the respective section within _print_at(...)

        :param x: The x coordinate
        :param y: The y coordinate
        """
        # Move the cursor
        if x != self._cur_x or y != self._cur_y:
            self._stdout.SetConsoleCursorPosition(
                win32console.PyCOORDType(x, y))

        # Update coordinates
        self._cur_x = x
        self._cur_y = y

    def _hide_cursor(self):
        self._stdout.SetConsoleCursorInfo(1, 0)

    def _show_cursor(self):
        self._stdout.SetConsoleCursorInfo(1, 1)
