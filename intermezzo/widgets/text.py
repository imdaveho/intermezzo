import time
from intermezzo.widgets import Question
from intermezzo.terminal.event import KeyboardEvent
from intermezzo.terminal import constants as cnst

class Text(Question):
    def __init__(self, name, query, labels=None):
        super().__init__(name, query, labels)
        self._type = "text"
        self._line_height = 2
        self._origin = (0, 0)
        self._coords = (0, 0)
        self._offset = (0, 0)
        # UNIX/POSIX specific
        # see _reset_cursor()
        self._typing = False
        self._timeout = time.time()

    def _display(self):
        query = self._labels['query'] + self.query
        self._offset = (0, self._line_number)

        # 1. Display the query
        if self._labels['query'] == '[?] ':
            query_colours = []
            for i, _ in enumerate(query):
                if i in (1,):
                    # bright green, normal, black
                    if type(self._screen).__name__ == '_WindowsScreen':
                        query_colours.append((2, 2, 0))
                    else:
                        query_colours.append((10, 2, 0))
                else:
                    # bright white, normal, black
                    if type(self._screen).__name__ == '_WindowsScreen':
                        query_colours.append((7, 2, 0))
                    else:
                        query_colours.append((15, 2, 0))
            self._print(query, colour_map=query_colours)
        else:
            #TODO: make colours configurable
            pass

        # 2. Display the prompt
        prompt = self._labels['prompt']
        if type(self._screen).__name__ == '_WindowsScreen':
            self._println(prompt, colour=1)
        else:
            self._println(prompt, colour=9)

        x, y = len(prompt), self._line_number + 1
        self._origin = (x, y)
        self._coords = (x, y)
        self._offset = (x, y)
        return None

    def _handle_event(self, evt):
        ENTER_KEY = 13
        DELETE_KEY = -102
        if isinstance(evt, KeyboardEvent):
            try:
                keyc = evt.key_code
                if keyc == ENTER_KEY:
                    # TODO: handle empty result if required field
                    full_length = len(self._result)
                    logged_result = self._result[:24]
                    if full_length > 24:
                        logged_result += "..."

                    x = len(self._labels['query'] + self.query) + 1
                    y = self._line_number
                    self._update_offset(xy=(x, y))
                    if type(self._screen).__name__ == '_WindowsScreen':
                        self._print(logged_result, colour=7)
                    else:
                        self._print(logged_result, colour=240)
                    self._update_offset(xy=(x, y+1))
                    self._clear_eos(reset=True)
                    self._typing = True
                    self.refresh()
                    return True

                elif keyc == cnst.KEY_BACK:
                    if self._coords[0] > self._origin[0]:
                        cx = self._coords[0] - self._origin[0]
                        self._update_coords(dx=-1)
                        self._result = self._result[:cx][:-1] + self._result[cx:]
                        self._clear_eol()

                elif keyc == DELETE_KEY:
                    cx = self._coords[0] - self._origin[0]
                    left_substr = self._result[:cx]
                    right_substr = self._result[cx:]
                    if len(right_substr) > 0:
                        self._result = left_substr + right_substr[1:]
                    self._clear_eol()
                    self._screen._move_cursor(self._coords[0] - 1, self._coords[1])

                elif keyc == cnst.KEY_LEFT:
                    if self._coords[0] > self._origin[0]:
                        self._update_coords(dx=-1)
                    x, y = self._coords
                    self._screen._move_cursor(x, y)

                elif keyc == cnst.KEY_RIGHT:
                    result = self._origin[0] + len(self._result)
                    if self._coords[0] < result:
                        self._update_coords(dx=1)
                    x, y = self._coords
                    self._screen._move_cursor(x, y)

                else:
                    try:
                        # TODO: implement word wrapping
                        char = ''
                        if chr(keyc).isprintable():
                            char = chr(keyc)
                        cx = self._coords[0] - self._origin[0]
                        self._result = self._result[:cx] + char + self._result[cx:]
                        self._typing = True
                        self._print(self._result)
                        self._update_coords(dx=1)

                    except ValueError:
                        pass
            except TypeError:
                pass
        else:
            pass
        return False

    def _print(self, text, colour=7, attr=2, bg=0, transparent=False, colour_map=None):
        screen = self._screen
        if not screen or screen == None:
            raise Exception("Screen instance not found.")
        config = {'colour': colour, 'attr': attr, 'bg': bg, 'transparent': transparent}
        try:
            x, y = self._offset
            if colour_map:
                screen.paint(text, x, y, colour_map=colour_map)
            else:
                screen.print_at(text, x, y, **config)
        except ValueError:
            pass
        return None

    def _println(self, text, colour=7, attr=2, bg=0, transparent=False, colour_map=None):
        screen = self._screen
        if not screen or screen == None:
            raise Exception("screen instance not found.")
        self._update_offset(dy=1)
        config = {'colour': colour, 'attr': attr, 'bg': bg, 'transparent': transparent}
        try:
            x, y = self._offset
            if colour_map:
                screen.paint(text, x, y, colour_map=colour_map)
            else:
                screen.print_at(text, x, y, **config)
        except ValueError:
            pass
        return None

    def _update_coords(self, dx=None, dy=None, xy=()):
        if not xy:
            x = self._coords[0] if dx is None else self._coords[0] + dx
            y = self._coords[1] if dy is None else self._coords[1] + dy
            self._coords = (x, y)
        else:
            self._coords = xy

    def _update_offset(self, dx=None, dy=None, xy=()):
        if not xy:
            x = self._offset[0] if dx is None else self._offset[0] + dx
            y = self._offset[1] if dy is None else self._offset[1] + dy
            self._offset = (x, y)
        else:
            self._offset = xy

    def _clear_eol(self, reset=False):
        w = self._screen.width
        clrx = ''.join([' ' for _ in range(0, w)])
        clip = len(self._result) + self._origin[0]

        self._typing = True
        if reset:
            self._screen.print_at(clrx, 0, self._offset[1])
            self._update_coords(xy=(0, self._offset[1]))
        else:
            self._print(self._result + clrx[clip:])

    def _clear_eos(self, reset=False):
        w, h = self._screen.width, self._screen.height
        # TODO: explain what overflow check is
        overflow_check = (h - 1) - (self._offset[1] + self._line_height)
        if overflow_check < 0:
            h += (self._line_height + 1)
        clrx =''.join([' ' for _ in range(0, w)])
        clry = [clrx for _ in range(self._offset[1] + 1, h)]

        # 1. clear line from current xpos
        clip = len(self._result) + self._origin[0]
        self._typing = True
        if reset:
            self._screen.print_at(clrx, 0, self._offset[1])
        else:
            self._print(self._result + clrx[clip:])
        # 2. clear subsequent lines below
        for i, ln in enumerate(clry):
            self._screen.print_at(ln, 0, self._offset[1] + i)

    def _reset_cursor(self):
        cx, cy = self._coords
        self._screen._move_cursor(cx, cy)

        if type(self._screen).__name__ == '_CursesScreen':
            if not self._typing:
                self._screen._show_cursor()
            else:
                self._screen._hide_cursor()

            if self._typing and (time.time() - self._timeout > self._frames_per_second):
                self._timeout = time.time()
                self._typing = False

    def _run(self):
        while True:
            evt = self._screen.get_event()
            if self._handle_event(evt):
                break
            self.refresh()

    def refresh(self):
        super().refresh()
        self._reset_cursor()
        self._update_offset(xy=self._origin)
        return None

    def ask(self, screen, ln):
        super().ask(screen, ln)
        response = {
            'result': self._result
        }
        return response
