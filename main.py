# import time
# from intermezzo.terminal.screen import Screen

# def render_loop(screen):
#     screen.print_at("Hello World! This is a test!", 0, 0, colour=30)
#     screen.refresh()
#     time.sleep(1)

# Screen.wrapper(render_loop)
# from intermezzo.console import Console
from intermezzo import Prompt
from intermezzo.widgets import Text

text = Text(name='name', query='What is your name?')
text2 = Text(name='email', query='What is your email?')
text3 = Text(name='phone', query='What is your phone?')
console = Prompt()
# console.load([text])
console.load_questions([text, text2, text3])
result = console.run()
print(result)
