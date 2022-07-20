import os
import re
from setuptools import setup, find_packages, dist, Extension

# get the local path of the installation files
LOCAL = os.path.dirname(os.path.realpath(__file__))

# options:
extra_compile_args = [
    "-fPIC",
    "-fno-strict-aliasing",
    "-D_LARGEFILE64_SOURCE=1",
    "-D_FILE_OFFSET_BITS=64",
    "-Isrc"
    # support SSE by default,
    # as the code can detect if it is available or not
    "-DFPNG_NO_SSE=0",
    "-msse4.1",
    "-mpclmul",
]

setup(
    name="fpng_py",
    description="",
    author="K0lb3",
    version="0.0.1",
    packages=find_packages(),
    long_description_content_type="text/markdown",
    install_requires=[],
    ext_modules=[
        Extension(
            "fpng_py._fpng_py",
            [
                "fpng_py/fpng_py.cpp",
                "fpng/src/fpng.cpp",
            ],
            language="c++",
            include_dirs=["fpng/src"],
            extra_compile_args=extra_compile_args,
        )
    ],
)
