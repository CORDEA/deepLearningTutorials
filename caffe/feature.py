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

# ref. http://techblog.yahoo.co.jp/programming/caffe-intro/

MEAN_FILE = 'python/caffe/imagenet/ilsvrc_2012_mean.npy'
MODEL_FILE = 'examples/imagenet/imagenet_feature.prototxt'
PRETRAINED = 'examples/imagenet/caffe_reference_imagenet_model'
FOLDER = '~/caffe/101_ObjectCategories/'
LAYER = 'fc6wi'
INDEX = 4

net = caffe.Classifier(MODEL_FILE, PRETRAINED)
net.set_phase_test()
net.set_mode_cpu()
net.set_mean('data', numpy.load(MEAN_FILE))
net.set_raw_scale('data', 255)
net.set_channel_swap('data', (2,1,0))


f = open(sys.argv[1], 'w')

species = 0
for dirname in  os.listdir(os.path.expanduser(FOLDER)):
    files = os.listdir(dirname)
    for filename in files:
        image = caffe.io.load_image(os.path.abspath(filename))
        net.predict([ image ])
        feat = net.blobs[LAYER].data[INDEX].flatten().tolist()
        number = 1
        feat_edit = []
        for fe in feat:
            feat_edit.append(str(number) + ':' + str(fe))
            number += 1
        f.write(' '.join([str(species)] + feat_edit) + '\n')
    species += 1

f.close()
