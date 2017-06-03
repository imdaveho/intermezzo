import os
from ._intermezzo import ffi, lib

class Intermezzo:
    def init():
        lib._Init()

    def close():
        lib._Close()
