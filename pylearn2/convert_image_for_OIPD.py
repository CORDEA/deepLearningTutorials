#!/usr/bin/env python
# encoding:utf-8
#
# Copyright 2015-2017 Yoshihiro Tanaka
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
import os, sys, random, re

_IMAGE_DIR = "images"       # images foloder path
_ANNO_DIR  = "annotations"  # annotations folder path
_SIZE      = 128, 128       # image size
_SMALL     = True
_DEL       = ','            # output file delimiter

def output(count, ID, data, files):
    if count == 1:
        files[1].write(
                str(ID) # Label information must be Number.
                + _DEL + data + '\n'
                )
    else:
        files[0].write(
                str(ID) # Label information must be Number.
                + _DEL + data + '\n'
                )

def main():
    classDict = {}
    with open(_ANNO_DIR + "/list.txt") as f:
        for line in f:
            if not '#' in line:
                items = line.rstrip().split()
                class_id = re.split("_[0-9]+", items[0])[0]
                if not class_id in classDict:
                    classDict[class_id] = items[1]

    train = open("train_small.csv", 'w')
    test  = open("test_small.csv", 'w')

    count = {}

    files = os.listdir(_IMAGE_DIR)
    for filename in files:
        class_id = re.split("_[0-9]+.jpg", filename)[0]

        input_image  = Image.open(path.join(_IMAGE_DIR, filename))
        resize_image = input_image.resize(_SIZE)
        #output_image = ImageOps.grayscale(resize_image)
        output_image = resize_image

        # ref. https://github.com/laughing/grbm_sample/blob/master/img2csv.py
        data = [str(int(r*100)) for r in (numpy.asarray(output_image).flatten() / 255.0).tolist()]
        if len(data) != _SIZE[0] * _SIZE[1] * 3: # RGB
            sys.stderr.write("error: %d\n" % (len(data)))
        else:
            data = _DEL.join(data)
            ID   = classDict[class_id]
            count[class_id] = count.get(class_id, 0) + 1

            if _SMALL:
                if count[class_id] <= 5:
                    output(count[class_id], ID, data, [train, test])
            else:
                output(count[class_id], ID, data, [train, test])
    train.close()
    test.close()


if __name__ == '__main__':
    main()
