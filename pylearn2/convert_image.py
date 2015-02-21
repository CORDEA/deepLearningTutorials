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

def convert_image(_PATH, _FILENAME, _SIZE, _COLOR):
    _DIR    = "in"
    _DEL    = ','

    train = open(_PATH + _FILENAME, 'w')
    comp  = open(_PATH + "comparative_table.name", 'w')

    dirs = os.listdir(_DIR + '/')

    label = 0
    for dirname in dirs:
        files = os.listdir(_DIR + '/' + dirname)
        for filename in files:
            input_image = Image.open(path.join(_DIR, dirname, filename))
            resize_image = input_image.resize(_SIZE, _SIZE)
            if _COLOR:
                output_image = resize_image
            else:
                output_image = ImageOps.grayscale(resize_image)
            # ref. https://github.com/laughing/grbm_sample/blob/master/img2csv.py
            data = _DEL.join([str(r) for r in (numpy.asarray(output_image).flatten() / 255.0).tolist()])
            train.write(
                    str(label) # Label information must be Number.
                    + _DEL + data + '\n'
                    )
            comp.write(' '.join([str(label), filename.rstrip(".png")]))
        label += 1
