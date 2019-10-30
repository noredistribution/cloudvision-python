#!/bin/bash
python setup.py sdist bdist_wheel
pip install --user  dist/AerisRequester-0.0.1-py3-none-any.whl
