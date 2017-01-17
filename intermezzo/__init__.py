import time
from intermezzo.terminal.event import KeyboardEvent
from intermezzo.terminal.screen import Screen
from intermezzo.fields import Question


class Prompt(object):
    def __init__(self):
        self._screen = None
        self._error_msg = ""
        self._line_number = 0
        self.index = 0
        self.questions = []
        self.result = {}

    def _check_viewport(self):
        screen = self._screen
        if not screen or screen == None:
            raise Exception("Screen instance not found.")
        if screen.width < 80 or screen.height < 24:
            return False
        return True

    def _ask_questions(self):
        # deepcopy so the object retains original list of questions after loop
        questions = [question for question in self.questions]
        if not len(questions):
            raise Exception("Nothing was loaded.")
        while questions:
            screen = self._screen
            question = questions.pop(0)
            response = question.ask(self._screen, self._line_number)
            self._line_number += 2

            # if 'skip' in response.keys() and 'iters' in response.keys():
            #     skip = response.get('skip')
            #     iters = response.get('iters')
            #     if skip and iters > 0:
            #         for i in range(iters):
            #             skipped_question = questions.pop(0)
            #             self.result[skipped_question.name] = None

            # update position from response for proper rendering of next question
            if self._line_number > self._screen.height - 1:
                diff = (self._line_number) - (screen.height - 1)
                self._screen.scroll_to(diff)

            # set result from response
            self.result[question.name] = response['result']

    def _is_done(self):
        results = self.result.items()
        questions = self.questions
        if len(results) == len(questions):
            return True
        return False

    def _inner_loop(self, screen):
        self._screen = screen
        if not self._check_viewport():
            while True:
                message = 'Resize window to at least 80(w)x24(h)'
                xpos, ypos = self._screen.width//2 - len(message)//2, self._screen.height//2
                self._screen.print_at(message, xpos, ypos)
                self._screen.refresh()
                if self._screen.has_resized():
                    break
            # skip below, re-render after minimum size
            return None
        self._ask_questions()
        # TODO: SHIFT + BACK => go back in questions
        # TODO: get results from summary tables and return them
        # TODO: ask how would you like your results? csv, xls, on screen
        time.sleep(0.8)
        return None

    def load_questions(self, data):
        dtype = type(data).__name__
        if dtype == 'Question':
            self.questions.append(data)
        elif dtype == 'list':
            names = set()
            for n in data:
                names.add(n.name)
                if not isinstance(n, Question):
                    error = 'Invalid parameter in the provided list. '
                    fix = 'Must be a list of Questions.'
                    raise Exception(error + fix)
            if len(names) != len(data):
                raise Exception('Question names are not unique.')
            self.questions = data
        else:
            error = 'Invalid parameter. '
            fix = 'Either pass in a Question or a list of Questions.'
            raise Exception(error + fix)
        return None

    def unload_questions(self):
        self.questions = []
        return None

    def run(self):
        while True:
            if self._is_done():
                break
            Screen.wrapper(self._inner_loop)
        return self.result
