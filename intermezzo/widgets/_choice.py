import time
from intermezzo.widgets import Question
from intermezzo.terminal.event import KeyboardEvent
from intermezzo.terminal import constants as cnst


class Choice(Question):
    def __init__(self, name, query, choices, size=7, labels=None):
        super().__init__(name, query, labels)
        self.choices = choices
        self._type = "choice"
        self._index = 0
        self._cursor = 0
        self._offset = (0, 0)
        self._segment = []
        self._list_size = size
        self._padding = size // 2
        self._bottom = len(choices) - 1
        self._line_height = size + 1

    def _display(self):
        query = self._labels['query'] + self.query
        self._offset = (0, self._line_number)
        if self._labels['query'] == '[?] ':
            query_colours = []
            for i, _ in enumerate(query):
                if i in (1,):
                    # bright green, normal, black
                    if self._os in ('win32',):
                        query_colours.append((2, 2, 0))
                    else:
                        query_colours.append((10, 2, 0))
                else:
                    # bright white, normal, black
                    if self._os in ('win32',):
                        query_colours.append((7, 2, 0))
                    else:
                        query_colours.append((15, 2, 0))
            self._print(query, colour_map=query_colours)
        else:
            #TODO: make colours configurable
            pass
        return None

    def _handle_event(self, evt):
        ENTER_KEY = 10
        if self._os in ('win32',):
            ENTER_KEY = 13
        if isinstance(evt, KeyboardEvent):
            try:
                keyc = evt.key_code
                if keyc == ENTER_KEY:
                    self._result = self.choices[self._index]
                    full_length = len(self._result)
                    logged_result = self._result[:24]
                    if full_length > 24:
                        logged_result += "..."
                    x = len(self._labels['query'] + self.query) + 1
                    y = self._line_number
                    self._update_offset(xy=(x, y))
                    if self._os in ('win32',):
                        self._print(logged_result, colour=7)
                    else:
                        self._print(logged_result, colour=240)
                    self._clear_eos()
                    self.refresh()
                    return True

                elif keyc == cnst.KEY_UP:
                    if self._cursor > self._padding:
                        self._cursor -= 1
                        self._index -= 1

                    elif self._index > self._padding:
                        self._index -= 1

                    elif self._index <= self._padding:
                        if self._index > 0:
                            self._index -= 1
                            self._cursor -= 1
                        else:
                            self._index = 0
                            self._pointer = 0
                    self._clear_eos()

                elif keyc == cnst.KEY_DOWN:
                    if self._cursor < self._padding:
                        self._cursor += 1
                        self._index += 1

                    elif self._index < self._bottom - self._padding:
                        self._index += 1

                    elif self._index >= self._bottom - self._padding:
                        if self._index < self._bottom:
                            self._index += 1
                            self._cursor += 1
                        else:
                            self._index = self._bottom
                            self._pointer = self._list_size - 1
                    self._clear_eos()

                else:
                    pass
            except TypeError:
                pass
        else:
            pass
        return False

    def _handle_segment(self):
        length = len(self.choices)
        if (length <= self._list_size):
            self._segment = self.choices
        start = self._index - self._cursor
        final = self._list_size + start
        self._segment = self.choices[start:final]
        return None

    def _update_offset(self, dx=None, dy=None, xy=()):
        if not xy:
            x = self._offset[0] if dx is None else self._offset[0] + dx
            y = self._offset[1] if dy is None else self._offset[1] + dy
            self._offset = (x, y)
        else:
            self._offset = xy

    def _handle_scroll(self):
        selector = self._labels['selector']
        blankspc = ''.join(" " for _ in range(len(selector)))
        aquamarine1, grey35 = 86, 240
        if self._os in ('win32',):
            aquamarine1, grey35 = 6, 7
        self._handle_segment()
        for i, choice in enumerate(self._segment):
            if i == self._cursor:
                self._println(selector + choice, colour=aquamarine1)
            else:
                self._println(blankspc + choice, colour=grey35)
        return None

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

    def _clear_eos(self):
        # TODO: generalize and consolidate to Question class
        w, h = self._screen.width, self._screen.height
        # TODO: explain what overflow check is
        overflow_check = (h - 1) - (self._offset[1] + self._line_height)
        if overflow_check < 0:
            h += (self._line_height + 1)
        clrx =''.join([' ' for _ in range(0, w)])
        clry = [clrx for _ in range(self._offset[1] + 1, h)]
        # choices are +1 from the query which gets reset to
        # self._line_number every loop
        choices_position = self._offset[1] + 1
        self._screen.print_at(clrx, 0, choices_position)
        for i, ln in enumerate(clry):
            self._screen.print_at(ln, 0, choices_position + i)

    def _run(self):
        while True:
            evt = self._screen.get_event()
            if self._handle_event(evt):
                break
            self._handle_scroll()
            self._update_offset(xy=(0, self._line_number))
            self.refresh()

    def ask(self, screen, ln):
        super().ask(screen, ln)
        response = {
            'result': self._result
        }
        return response
