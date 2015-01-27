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
__date__   =  "2015-01-27"

# for The Oxford-IIIT Pet Dataset.
# Link: http://www.robots.ox.ac.uk/~vgg/data/pets/

import numpy
from PIL import Image, ImageOps
from os import path
import os

_IMAGE_DIR = "images"
_ANNO_DIR  = "annotations"
_SIZE      = 256, 256

classDict = {}
with open(_ANNO_DIR + "/list.txt") as f:
    for line in f:
        if not '#' in line:
            items = line.rstrip().split()
            class_id = items[0].split('_')[0]
            if not class_id in classDict:
                classDict[class_id] = items[1]

train = open("train.txt", 'w')

files = os.listdir(_IMAGE_DIR)
for filename in files:
    class_id = filename.split('_')[0]

    input_image  = Image.open(path.join(_IMAGE_DIR, filename))
    resize_image = input_image.resize(_SIZE)
    #output_image = ImageOps.grayscale(resize_image)
    output_image = resize_image

    # ref. https://github.com/laughing/grbm_sample/blob/master/img2csv.py
    data = ' '.join([str(r) for r in (numpy.asarray(output_image).flatten() / 255.0).tolist()])
    train.write(
            str(classDict[class_id]) # Label information must be Number.
            + ',' + data + '\n'
            )
train.close()
