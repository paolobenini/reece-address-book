import setuptools
from pathlib import Path

setuptools.setup(
    name = "reece_address_book",
    version = "1.0.0",
    author = "Paolo Benini",
    description = "A simple project for an address book API",
    long_description = Path("README.md").read_text(),
    long_description_content_type = "text/markdown",
    packages = setuptools.find_packages(include = ["reece_address_book"]),
)