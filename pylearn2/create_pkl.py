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

import sys
import pickle
from pylearn2.datasets.csv_dataset import CSVDataset

__Author__ = "Yoshihiro Tanaka"
__date__ = "2015-01-23"

# ref. http://tanopy.blog79.fc2.com/blog-entry-118.html
try:
    data = CSVDataset(
        path=sys.argv[1] + '.csv', expect_headers=False, one_hot=True)
except:
    data = CSVDataset(path=sys.argv[1] + '.csv', expect_headers=False)
pickle.dump(data, open(sys.argv[1] + '.pkl', 'w'))
