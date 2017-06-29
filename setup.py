import platform
from setuptools import setup

if platform.system() == "Windows":
    setup(
        name="intermezzo",
        version="0.1.0",
        description="A library for creating cross-platform text-based interfaces using termbox-go.",
        long_description="",
        url="https://github.com/imdaveho/intermezzo",
        author="Dave Ho",
        author_email="imdaveho@gmail.com",
        license="MIT",
        classifiers=[],
        packages=["intermezzo"],
        package_data={"intermezzo": ["build/*/*.dll"]},
        keywords="termbox tui terminal command-line",
        install_requires=["cffi>=1.10.0"],
        cffi_modules=["intermezzo/build/build_ffi_win.py:ffi"],
        setup_requires=["cffi>=1.10.0"],
        )
else:
    setup(
        name="intermezzo",
        version="0.1.0",
        description="A library for creating cross-platform text-based interfaces using termbox-go.",
        long_description="",
        url="https://github.com/imdaveho/intermezzo",
        author="Dave Ho",
        author_email="imdaveho@gmail.com",
        license="MIT",
        classifiers=[],
        packages=["intermezzo"],
        package_data={"intermezzo": ["build/*/*.so"]},
        keywords="termbox tui terminal command-line",
        install_requires=["cffi>=1.10.0"],
        cffi_modules=["intermezzo/build/build_ffi_nix.py:ffi"],
        setup_requires=["cffi>=1.10.0"],
        )
