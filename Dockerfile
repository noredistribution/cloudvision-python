FROM ubuntu:20.04
LABEL maintainer="Ethan Seither eseither@arista.com"

RUN apt-get update
RUN apt-get -y install git=1:2.25* make=4.2.1*

# peg to specific versions from 20.04 LTS, see https://packages.ubuntu.com/focal/python/
RUN apt-get -y install python3-msgpack=0.6.2* python3-protobuf=3.6.1.3* \
    python3-numpy=1:1.17.4* python3-yaml=5.3.1* python3-pytest=4.6.9* \
    python3-pip=20.0.2* python3-grpcio=1.16.1*

ARG DOCKER_BUILD_COMMIT

COPY ./ /python/cloudvision-python
