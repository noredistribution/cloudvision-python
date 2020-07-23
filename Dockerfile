FROM python:3.8
LABEL maintainer="Ethan Seither eseither@arista.com"

RUN python -m pip install msgpack==0.6.2 protobuf==3.12.2 \
    numpy==1.17.4 pyyaml==5.3.1 pytest==4.6.9 \
    grpcio==1.30.0
