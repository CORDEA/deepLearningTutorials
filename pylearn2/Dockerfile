# Not tried. Therefore, I dont know if it will works.
FROM ubuntu:14.04

MAINTAINER Yoshihiro Tanaka <feria.primavera@gmail.com>


RUN apt-get -y update && \
    apt-get install -y python wget vim git && \
    apt-get install -y make bc libprotobuf-dev libleveldb-dev libsnappy-dev libopencv-dev libboost-all-dev libhdf5-serial-dev libblas-dev libatlas-base-dev libgflags-dev libgoogle-glog-dev liblmdb-dev protobuf-compiler libsvm-dev libsvm3 libsvm-toolset && \
    apt-get install -y python-setuptools python-pip python-dev python-numpy python-scipy python-yaml python-matplotlib liblapack-dev python-nose2 cython

RUN adduser --disabled-password --gecos '' huge && \
    adduser huge sudo && \
    echo '%sudo ALL=(ALL) NOPASSWD:ALL' >> /etc/sudoers

USER huge
ENV HOME /home/huge:/pylearn2/pylearn2/scripts
ENV PYLEARN2_DATA_PATH $HOME/.data/lisa/data

RUN sudo pip install theano

WORKDIR $HOME
RUN git clone https://github.com/lisa-lab/pylearn2.git
WORKDIR $HOME/pylearn2
RUN sudo python setup.py develop



ENTRYPOINT ["/bin/bash"]
