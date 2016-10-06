# UNIX compatible platform - use curses
import sys
import signal
from intermezzo.console import Screen
from intermezzo import constants as cnst
from intermezzo.event import KeyboardEvent, MouseEvent
from locale import getlocale, getdefaultlocale

import curses

# Handle terminals in UNIX based systems (Linux/BSD/MacOS)

def open(cls, height=200, catch_interrupt=False, unicode_aware=None):
    # Reproduce curses.wrapper()
    stdscr = curses.initscr()
    curses.noecho()
    curses.cbreak()
    stdscr.keypad(1)

    # noinspection PyBroadException
    # pylint: disable=bare-except
    # - This code deliberately duplicates the (bad) curses module code.
    try:
        curses.start_color()
    except:
        pass
    screen = _CursesScreen(stdscr, height,
                           catch_interrupt=catch_interrupt,
                           unicode_aware=unicode_aware)
    return screen


class _CursesScreen(Screen):
    """
    Curses screen implementation.
    """

    # Virtual key code mapping.
    _KEY_MAP = {
        27: cnst.KEY_ESCAPE,
        curses.KEY_F1: cnst.KEY_F1,
        curses.KEY_F2: cnst.KEY_F2,
        curses.KEY_F3: cnst.KEY_F3,
        curses.KEY_F4: cnst.KEY_F4,
        curses.KEY_F5: cnst.KEY_F5,
        curses.KEY_F6: cnst.KEY_F6,
        curses.KEY_F7: cnst.KEY_F7,
        curses.KEY_F8: cnst.KEY_F8,
        curses.KEY_F9: cnst.KEY_F9,
        curses.KEY_F10: cnst.KEY_F10,
        curses.KEY_F11: cnst.KEY_F11,
        curses.KEY_F12: cnst.KEY_F12,
        curses.KEY_F13: cnst.KEY_F13,
        curses.KEY_F14: cnst.KEY_F14,
        curses.KEY_F15: cnst.KEY_F15,
        curses.KEY_F16: cnst.KEY_F16,
        curses.KEY_F17: cnst.KEY_F17,
        curses.KEY_F18: cnst.KEY_F18,
        curses.KEY_F19: cnst.KEY_F19,
        curses.KEY_F20: cnst.KEY_F20,
        curses.KEY_F21: cnst.KEY_F21,
        curses.KEY_F22: cnst.KEY_F22,
        curses.KEY_F23: cnst.KEY_F23,
        curses.KEY_F24: cnst.KEY_F24,
        curses.KEY_PRINT: cnst.KEY_PRINT_SCREEN,
        curses.KEY_IC: cnst.KEY_INSERT,
        curses.KEY_DC: cnst.KEY_DELETE,
        curses.KEY_HOME: cnst.KEY_HOME,
        curses.KEY_END: cnst.KEY_END,
        curses.KEY_LEFT: cnst.KEY_LEFT,
        curses.KEY_UP: cnst.KEY_UP,
        curses.KEY_RIGHT: cnst.KEY_RIGHT,
        curses.KEY_DOWN: cnst.KEY_DOWN,
        curses.KEY_PPAGE: cnst.KEY_PAGE_UP,
        curses.KEY_NPAGE: cnst.KEY_PAGE_DOWN,
        curses.KEY_BACKSPACE: cnst.KEY_BACK,
        9: cnst.KEY_TAB,
        curses.KEY_BTAB: cnst.KEY_BACK_TAB,
        # Terminals translate keypad keys, so no need for a special
        # mapping here.

        # Terminals don't transmit meta keys (like control, shift, etc), so
        # there's no translation for them either.
    }

    def __init__(self, win, height=200, catch_interrupt=False,
                 unicode_aware=False):
        """
        :param win: The window object as returned by the curses wrapper
            method.
        :param height: The height of the screen buffer to be used.
        :param catch_interrupt: Whether to catch SIGINT or not.
        :param unicode_aware: Whether this Screen can use unicode or not.
        """
        # Determine unicode support if needed.
        if unicode_aware is None:
            encoding = getlocale()[1]
            if not encoding:
                encoding = getdefaultlocale()[1]
            unicode_aware = (encoding is not None and
                             encoding.lower() == "utf-8")

        # Save off the screen details.
        super(_CursesScreen, self).__init__(
            win.getmaxyx()[0], win.getmaxyx()[1], height, unicode_aware)
        self._screen = win
        self._screen.keypad(1)

        # Set up basic colour schemes.
        self.colours = curses.COLORS

        # Disable the cursor.
        curses.curs_set(0)

        # Non-blocking key checks.
        self._screen.nodelay(1)

        # Set up signal handler for screen resizing.
        self._re_sized = False
        signal.signal(signal.SIGWINCH, self._resize_handler)

        # Catch SIGINTs and translated them to ctrl-c if needed.
        if catch_interrupt:
            # Ignore SIGINT (ctrl-c) and SIGTSTP (ctrl-z) signals.
            signal.signal(signal.SIGINT, self._catch_interrupt)
            signal.signal(signal.SIGTSTP, self._catch_interrupt)

        # Enable mouse events
        curses.mousemask(curses.ALL_MOUSE_EVENTS |
                         curses.REPORT_MOUSE_POSITION)

        # Lookup the necessary escape codes in the terminfo database.
        self._move_y_x = curses.tigetstr("cup")
        self._up_line = curses.tigetstr("ri").decode("utf-8")
        self._down_line = curses.tigetstr("ind").decode("utf-8")
        self._fg_color = curses.tigetstr("setaf")
        self._bg_color = curses.tigetstr("setab")
        if curses.tigetflag("hs"):
            self._start_title = curses.tigetstr("tsl").decode("utf-8")
            self._end_title = curses.tigetstr("fsl").decode("utf-8")
        else:
            self._start_title = self._end_title = None
        self._a_normal = curses.tigetstr("sgr0").decode("utf-8")
        self._a_bold = curses.tigetstr("bold").decode("utf-8")
        self._a_reverse = curses.tigetstr("rev").decode("utf-8")
        self._a_underline = curses.tigetstr("smul").decode("utf-8")
        self._clear_screen = curses.tigetstr("clear").decode("utf-8")

        # Conversion from Screen attributes to curses equivalents.
        self._ATTRIBUTES = {
            cnst.A_BOLD: self._a_bold,
            cnst.A_NORMAL: self._a_normal,
            cnst.A_REVERSE: self._a_reverse,
            cnst.A_UNDERLINE: self._a_underline
        }

        # Byte stream processing for unicode input.
        self._bytes_to_read = 0
        self._bytes_to_return = b""

        # We'll actually break out into low-level output, so flush any
        # high level buffers now.
        self._screen.refresh()

    def close(self, restore=True):
        """
        Close down this Screen and tidy up the environment as required.

        :param restore: whether to restore the environment or not.
        """
        if restore:
            self._screen.keypad(0)
            curses.echo()
            curses.nocbreak()
            curses.endwin()

    @staticmethod
    def _safe_write(msg):
        """
        Safe write to screen - catches IOErrors on screen resize.

        :param msg: The message to write to the screen.
        """
        try:
            sys.stdout.write(msg)
        except IOError:
            # Screen resize can throw IOErrors.  These can be safely
            # ignored as the screen will be shortly reset anyway.
            pass

    def _resize_handler(self, *_):
        """
        Window resize signal handler.  We don't care about any of the
        parameters passed in beyond the object reference.
        """
        curses.endwin()
        curses.initscr()
        self._re_sized = True

    def _scroll(self, lines):
        """
        Scroll the window up or down.

        :param lines: Number of lines to scroll.  Negative numbers scroll
            down.
        """
        if lines < 0:
            self._safe_write("{}{}".format(
                curses.tparm(self._move_y_x, 0, 0).decode("utf-8"),
                self._up_line * -lines))
        else:
            self._safe_write("{}{}".format(curses.tparm(
                self._move_y_x, self.height, 0).decode("utf-8"),
                self._down_line * lines))

    def _clear(self):
        """
        Clear the Screen of all content.
        """
        self._safe_write(self._clear_screen)
        sys.stdout.flush()

    def refresh(self):
        """
        Refresh the screen.
        """
        super(_CursesScreen, self).refresh()
        try:
            sys.stdout.flush()
        except IOError:
            pass

    @staticmethod
    def _catch_interrupt(signal_no, frame):
        """
        SIGINT handler.  We ignore the signal and frame info passed in.
        """
        # Stop pep-8 shouting at me for unused params I can't control.
        del frame

        # The OS already caught the ctrl-c, so inject it now for the next
        # input.
        if signal_no == signal.SIGINT:
            curses.ungetch(3)
        elif signal_no == signal.SIGTSTP:
            curses.ungetch(26)
        return

    def get_event(self):
        """
        Check for an event without waiting.
        """
        # Spin through notifications until we find something we want.
        key = 0
        while key != -1:
            # Get the next key
            key = self._screen.getch()

            if key == curses.KEY_RESIZE:
                # Handle screen resize
                self._re_sized = True
            elif key == curses.KEY_MOUSE:
                # Handle a mouse event
                _, x, y, _, bstate = curses.getmouse()
                buttons = 0
                # Some Linux modes only report clicks, so check for any
                # button down or click events.
                if (bstate & curses.BUTTON1_PRESSED != 0 or
                        bstate & curses.BUTTON1_CLICKED != 0):
                    buttons |= MouseEvent.LEFT_CLICK
                if (bstate & curses.BUTTON3_PRESSED != 0 or
                        bstate & curses.BUTTON3_CLICKED != 0):
                    buttons |= MouseEvent.RIGHT_CLICK
                if bstate & curses.BUTTON1_DOUBLE_CLICKED != 0:
                    buttons |= MouseEvent.DOUBLE_CLICK
                return MouseEvent(x, y, buttons)
            elif key != -1:
                # Handle any byte streams first
                logger.debug("Processing key: %x", key)
                if self._unicode_aware and key > 0:
                    if key & 0xC0 == 0xC0:
                        self._bytes_to_return = struct.pack(b"B", key)
                        self._bytes_to_read = bin(key)[2:].index("0") - 1
                        logger.debug("Byte stream: %d bytes left",
                                     self._bytes_to_read)
                        continue
                    elif self._bytes_to_read > 0:
                        self._bytes_to_return += struct.pack(b"B", key)
                        self._bytes_to_read -= 1
                        if self._bytes_to_read > 0:
                            continue
                        else:
                            key = ord(self._bytes_to_return.decode("utf-8"))

                # Handle a genuine key press.
                logger.debug("Returning key: %x", key)
                if key in self._KEY_MAP:
                    return KeyboardEvent(self._KEY_MAP[key])
                elif key != -1:
                    return KeyboardEvent(key)

        return None

    def has_resized(self):
        """
        Check whether the screen has been re-sized.
        """
        re_sized = self._re_sized
        self._re_sized = False
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
        if attr != self._attr:
            self._safe_write(self._a_normal)
            if attr != 0:
                self._safe_write(self._ATTRIBUTES[attr])
            self._attr = attr
            self._colour = None
            self._bg = None

        # Now swap colours if required.
        if colour != self._colour:
            self._safe_write(curses.tparm(
                self._fg_color, colour).decode("utf-8"))
            self._colour = colour
        if bg != self._bg:
            self._safe_write(curses.tparm(
                self._bg_color, bg).decode("utf-8"))
            self._bg = bg

    def _print_at(self, text, x, y):
        """
        Print string at the required location.

        :param text: The text string to print.
        :param x: The x coordinate
        :param y: The Y coordinate
        """
        # Move the cursor if necessary
        cursor = u""
        if x != self._x or y != self._y:
            cursor = curses.tparm(self._move_y_x, y, x).decode("utf-8")

        # Print the text at the required location and update the current
        # position.
        try:
            self._safe_write(cursor + text)
        except UnicodeEncodeError:
            # This is probably a sign that the user has the wrong locale.
            # Try to soldier on anyway.
            self._safe_write(cursor + "?" * len(text))

    def set_title(self, title):
        """
        Set the title for this terminal/console session.  This will
        typically change the text displayed in the window title bar.

        :param title: The title to be set.
        """
        if self._start_line is not None:
            self._safe_write("{}{}{}".format(self._start_title, title,
                                             self._end_title))
