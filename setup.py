from os import path

from setuptools import find_packages, setup

working_directory = path.abspath(path.dirname(__file__))

with open(path.join(working_directory, "README.md"), encoding="utf-8") as f:
    long_description = f.read()


setup(
    name="diff-tracer",
    version="0.0.1",
    description="Compare two responses to see if there is any difference or if both are having identical properties and values.",
    package_dir={"": "diff-tracer"},
    packages=find_packages(where="diff-tracer"),
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://github.com/betofigueiredo/diff-tracer",
    author="Herberto Figueiredo",
    author_email="herbertof@gmail.com",
    license="MIT",
    classifiers=[
        "License :: OSI Approved :: MIT License",
        "Programming Language :: Python :: 3.10",
        "Operating System :: OS Independent",
    ],
    install_requires=[],
    extras_require={
        # "dev": ["pytest>=7.0", "twine>=4.0.2"],
    },
    python_requires=">=3.10",
)
