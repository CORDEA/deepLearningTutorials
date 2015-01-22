#!/usr/bin/env python
# encoding:utf-8
#
# Copyright [2015] [Yoshihiro Tanaka]
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#   http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.

__Author__ =  "Yoshihiro Tanaka"
__date__   =  "2015-01-22"

import sys, os, numpy, caffe
from os import path


def getPATH(PATH):
    return path.expanduser(PATH)

def main():
    # ref. http://techblog.yahoo.co.jp/programming/caffe-intro/
    MEAN_FILE  = getPATH('~/caffe/python/caffe/imagenet/ilsvrc_2012_mean.npy')
    MODEL_FILE = getPATH('~/caffe/examples/imagenet/imagenet_feature.prototxt')
    PRETRAINED = getPATH('~/caffe/examples/imagenet/caffe_reference_imagenet_model')
    FOLDER     = getPATH('~/caffe/101_ObjectCategories/')

    LAYER = 'fc6wi'
    INDEX = 4

    net = caffe.Classifier(MODEL_FILE, PRETRAINED)
    net.set_phase_test()
    net.set_mode_cpu()
    net.set_mean('data', numpy.load(MEAN_FILE))
    net.set_raw_scale('data', 255)
    net.set_channel_swap('data', (2,1,0))

    train = open("train.txt", 'w')
    test  = open("test.txt", 'w')
    comp  = open("comparative_table.name", 'w')

    species = 0
    for dirname in  os.listdir(FOLDER):
        files = os.listdir(FOLDER + '/' + dirname)
        comp.write(' '.join([str(species), dirname]))
        testFlag = True
        for filename in files:
            image = caffe.io.load_image(path.join(FOLDER, dirname, filename))
            net.predict([ image ])
            feat = net.blobs[LAYER].data[INDEX].flatten().tolist()
            number = 1
            feat_edit = []
            for fe in feat:
                feat_edit.append(str(number) + ':' + str(fe))
                number += 1

            if testFlag:
                test.write(' '.join([str(species)] + feat_edit) + '\n')
                testFlag = False
            else:
                train.write(' '.join([str(species)] + feat_edit) + '\n')
        species += 1

    train.close()
    test.close()
    comp.close()

if __name__=="__main__":
    main()
