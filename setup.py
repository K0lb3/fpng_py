from setuptools import setup, find_packages, Extension

with open("README.md", "r") as fh:
    long_description = fh.read()

# options:
extra_compile_args = [
    # use Python's limited api for C++
    # allows building wheels for all python (3) versions
    "-DPy_LIMITED_API=0x03060000",
    # fpng args
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
    version="0.0.2",
    keywords=["png", "compression"],
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
        "Intended Audience :: Developers",
        "Programming Language :: Python",
        "Programming Language :: Python :: 3",
        "Topic :: Multimedia :: Graphics",
    ],
    url="https://github.com/K0lb3/fpng_py",
    download_url="https://github.com/K0lb3/fpng_py/tarball/master",
    packages=find_packages(),
    long_description=long_description,
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
