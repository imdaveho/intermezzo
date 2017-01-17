import time


class Question(object):
    def __init__(self, name, query, labels=None):
        self.name = name
        self.query = query
        self._type = None
        self._screen = None
        self._result = ""
        self._line_number = 0
        self._timer = time.time()
        self._labels = self._config(labels)
        self._frames_per_second = 1./80

    def _config(self, labels):
        if labels is None:
            labels = {}
        query = labels.get('query') or "[?]"
        # RIGHT-POINTING DOUBLE ANGLE QUOTATION MARK
        prompt = labels.get('prompt') or "\u00BB"
        # RADIO FILLED (FISHEYE)
        toggle = labels.get('toggle') or "\u25C9"
        # RADIO BLANK (LARGE CIRCLE)
        untoggle = labels.get('untoggle') or "\u25EF"
        # SINGLE RIGHT-POINTING ANGLE QUOTATION MARK
        selector = labels.get('selector') or "\u203A"
        config = {
            'query': query + " ",
            'prompt': " " + prompt + " ",
            'toggle': toggle + " ",
            'untoggle': untoggle + " ",
            'selector': " " + selector + " "
        }
        return config

    def _display(self):
        pass

    def _run(self):
        pass

    def throttle(self, fps=None):
        if fps is not None:
            self._frames_per_second = 1./fps
        threshold = self._frames_per_second
        delay = max(threshold - (time.time() - self._timer), 0)
        time.sleep(delay)
        return None

    def refresh(self):
        self._timer = time.time()
        self._screen.refresh()
        self.throttle()
        return None

    def ask(self, screen, ln):
        # Pass the Prompt parameters
        self._screen = screen
        self._line_number = ln
        # Display the prompt and run
        self._display()
        self._run()
        return None

from intermezzo.widgets.text import Text
