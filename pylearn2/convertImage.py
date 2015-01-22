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

_OUTDIR = "out"
_SIZE   = 128, 128

if not os.path.exists(_OUTDIR + "/"):
    os.system("mkdir " + _OUTDIR)

ls = os.listdir("in/")

with open(sys.argv[1]) as f:
    for filename in ls:
        input_image = Image.open("in/" + filename)
        resize_image = input_image.resize(_SIZE)
        output_image = ImageOps.grayscale(resize_image)
        # output_image.save(_OUTDIR + "/" + filename)
        data = ' '.join([str(r) for r in (numpy.asarray(output_image).flatten() / 255.0).tolist()])
        f.write(filename + ',' + data + '\n')
