print("compile.py")

from distutils.core import setup
import py2exe

setup(
    options={"py2exe": {"bundle_files":3}},

    windows=['jdle.py']
)