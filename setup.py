from setuptools import setup, find_packages

setup(name="intermezzo",
      version="1.0.0",
      description="A library for creating cross-platform text-based interfaces using termbox-go.",
      url="https://github.com/imdaveho/intermezzo",
      author="Dave Ho",
      author_email="imdaveho@gmail.com",
      license="MIT",
      packages=find_packages(),
      keywords="termbox tui terminal command-line",
      install_requires=["cffi>=1.10.0"],
      cffi_modules=["build/tbx_build.py:ffibuilder"],
      setup_requires=["cffi>=1.10.0"],
)
