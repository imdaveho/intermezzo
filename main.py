import time
from intermezzo.console import Screen

def render_loop(screen):
    screen.print_at("Hello World! This is a test!", 0, 0, colour=30)
    screen.refresh()
    time.sleep(1)

Screen.wrapper(render_loop)
