#!/bin/bash
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
#
# Author: Yoshihiro Tanaka
# date: 2015-01-22

aftfile="caffe_io"

for file in `find . -name "*.py"`; do
    sed -i -e "s/import [\w\.]*io/import $aftfile/g" $file
    sed -i -e "s/caffe\.io/caffe\.$aftfile/g" $file
done

mv "caffe/io.py" "caffe/"$aftfile".py"
