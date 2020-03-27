"""Import readme and create package info."""
import setuptools

with open("README.md", "r") as fh:
    long_description = fh.read()

setuptools.setup(
    name="cloudvision",
    version="0.0.1",
    description="A Python library for Arista's CloudVision APIs.",
    maintainer_email="support@arista.com",
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
