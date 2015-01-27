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

import numpy
from PIL import Image, ImageOps
import os, sys

_DIR    = "in"
_SIZE   = 128, 128
_DEL    = ','

dirs = os.listdir(_DIR + '/')
train = open("train.csv", 'w')
comp  = open("comparative_table.name", 'w')

label = 0
with open(sys.argv[1], 'w') as f:
    for dirname in dirs:
        files = os.listdir(_DIR + '/' + dirname)
        for filename in files:
            input_image = Image.open(path.join(_DIR, dirname, filename))
            resize_image = input_image.resize(_SIZE)
            output_image = ImageOps.grayscale(resize_image)
            # ref. https://github.com/laughing/grbm_sample/blob/master/img2csv.py
            data = _DEL.join([str(r) for r in (numpy.asarray(output_image).flatten() / 255.0).tolist()])
            train.write(
                    str(label) # Label information must be Number.
                    + _DEL + data + '\n'
                    )
            comp.write(' '.join([str(label), filename.rstrip(".png")]))
        label += 1
