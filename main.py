# import time
# from intermezzo.terminal.screen import Screen

# def render_loop(screen):
#     screen.print_at("Hello World! This is a test!", 0, 0, colour=30)
#     screen.refresh()
#     time.sleep(1)

# Screen.wrapper(render_loop)
# from intermezzo.console import Console
from intermezzo import Prompt
from intermezzo.fields import Text, Password, Choice, Multiple

text = Text(name='name', query='What is your name?')
text2 = Text(name='email', query='What is your email?')
pass1 = Password(name='pass', query='What is your password?')
choices1 = ['free', 'amateur', 'enthusiast', 'advanced', 'pro', 'mid-scale', 'enterprise', 'custom']
choice1 = Choice(name='tier', query='Which pricing tier do you want to purchase?', choices=choices1)
choices2 = ['0-10', '11-50', '51-150', '150-300', '300+']
choice2 = Choice(name='employees', query='How many employees do you have?', choices=choices2)
console = Prompt()
multichoices1 = ['Finance', 'Legal', 'Marketing', 'Tech', 'Product', 'HR', 'Operations', 'Administration', 'Manufacturing', 'Sales']
multichoice1 = Multiple(name='dept', query='Which departments will use this? (Select multiple)', choices=multichoices1)
# console.load([text])
console.load_questions([text, text2, pass1, choice1, choice2, multichoice1])
result = console.run()
print(result)
