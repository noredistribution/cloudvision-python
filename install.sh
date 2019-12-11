#!/bin/bash
python3 setup.py sdist bdist_wheel
pip3 install --user --force-reinstall dist/AerisRequester-0.0.1-py3-none-any.whl
