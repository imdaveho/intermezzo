# intermezzo
Cross platform library to build command line user experiences.

## Table of Contents

* [Goal and Purpose](#goal)
  - [Why?](#why)
* [Documentation](#documentation)
  - [Installation](#installation)
  - [Examples](#examples)
  - [Prompt Types](#types)
* [Credits](#credits)
  - [termbox-go](#termbox-go)
  - [asciimatics](#asciimatics)
* [License](#license)
  
## [Goal and Purpose](#goal)
Python is cross platform, so why shouldn't the tools that interact with the command line also be? Intermezzo provides a simple API to create terminal based user experiences. It takes the ergonomics of Python and combines it with the cross platform flexibility of Golang. Intermezzo is a thin wrapper around the simple, but powerful Termbox(-Go) library--which is a modern replacement for [curses](docs.python.org/3/library/curses.html)/[blessings](github.com/erikrose/blessings) and [pypiwin32](github.com/pywin32/pypiwin32)

### [Why?](#why)
Curses/Blessings only works on Linux and BSD terminals. On Windows, there is little to no support/documentation is hard to grok. Additionally, there was nothing that kept the API consistent across both platforms. (Believe me, I've checked) Of course, there are specialized libraries out there like [Colorama](github.com/tartley/colorama) and [Python Prompt Toolkit](github.com/jonathanslenders/python-prompt-toolkit), but I felt they were overly complex and/or niche. 

When I came across Peter Brittain's [asciimatics](#), it was incredibly straight forward and intuitive. I wanted something similar to what he did with [screen.py](github.com/peterbrittain/asciimatics/blob/master/asciimatics/screen.py), but without all the other bells and whistles and fancy effects of the library. Then I came across [termbox](github.com/nsf/termbox) and, more recently, [termbox-go](github.com/nsf/termbox-go). There is a proliferation of projects already built on top of termbox-go. The problem? Well...for most CLI applications, Go might be a bit overkill. How could we optimize for developer speed and productivity? (eg. with Python, Ruby, Node, etc) With Go 1.5+, `go build` allows for the building of shared C libraries that could be interfaced through FFI. This means that in theory, termbox-go could be ported to any language that has solid FFI with C.

Here is the Python version using CFFI. (feel free to use this as a reference)

## [Documentation](#documentation)
TDB.

## [Credits](#credits)
- Have got to thank the amazing [nsf](github.com/nsf) for providing an excellent library for working with command line interfaces.
- Many thanks to [peterbrittain](github.com/peterbrittain) for the initial iteration of Intermezzo based on his [screen.py](github.com/peterbrittain/asciimatics/blob/master/asciimatics/screen.py) implementation.
- Couldn't have done it without this guide written by Andrey Petrov ([shazow](github.com/shazow)): [See Python, See Python Go, Go Python Go](blog.heroku.com/see_python_see_python_go_go_python_go) as well as the guide by [Filippo Valsorda](blog.filippo.io): [Building Python Modules with Go 1.5](blog.filippo.io/building-python-modules-with-go-1-5)

## [License](#license)
Copywrite (c) 2016-2017 David Ho. Licensed under the MIT license.
