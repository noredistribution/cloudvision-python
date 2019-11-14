"""Import readme and create package info."""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="AerisRequester",
    version="0.0.1",
    author="lgroux",
    author_email="lgroux@arista.com",
    description="A python module to query date from aeris through grpc",
    long_description=long_description,
    long_description_content_type="text/markdown",
    url="https://gitlab.aristanetworks.com/lgroux/AerisRequester",
    packages=setuptools.find_packages(),
    classifiers=[
        "Programming Language :: Python :: 3",
        "License :: OSI Approved :: MIT License",
        "Operating System :: OS Independent",
    ],
)
