"""
Yoshihiro Tanaka has modified several points for my programs.
forked from https://github.com/laughing/grbm_sample
"""

__authors__    = ["Ian Goodfellow", "Yoshihiro Tanaka <feria.primavera@gmail.com>"]
__copyright__  = "Copyright 2013, Universite de Montreal"
__credits__    = ["Ian Goodfellow", "Yoshihiro Tanaka <feria.primavera@gmail.com>"]
__license__    = "3-clause BSD"
__maintainer__ = "Yoshihiro Tanaka <feria.primavera@gmail.com>"

import csv
import numpy as np
import os

from pylearn2.datasets.dense_design_matrix import DefaultViewConverter
from pylearn2.datasets.dense_design_matrix import DenseDesignMatrix
from pylearn2.utils.string_utils import preprocess
from convert_image import convert_image

class HogeDataset(DenseDesignMatrix):
    def __init__(self,
            which_set,
            base_path               = '${PYLEARN2_DATA_PATH}/hoge',
            start                   = None,
            stop                    = None,
            preprocessor            = None,
            fit_preprocessor        = False,
            axes                    = ('b', 0, 1, 'c'),
            fit_test_preprocessor   = False,
            image_to_csv            = False
            ):
        """
        which_set: A string specifying which portion of the dataset
            to load. Valid values are 'train' or 'public_test'
        base_path: The directory containing the .csv files from kaggle.com.
                This directory should be writable; if the .csv files haven't
                already been converted to npy, this class will convert them
                to save memory the next time they are loaded.
        fit_preprocessor: True if the preprocessor is allowed to fit the
                   data.
        fit_test_preprocessor: If we construct a test set based on this
                    dataset, should it be allowed to fit the test set?
        """

        self.test_args = locals()
        self.test_args['which_set'] = 'public_test'
        self.test_args['fit_preprocessor'] = fit_test_preprocessor
        del self.test_args['start']
        del self.test_args['stop']
        del self.test_args['self']

        filename = which_set + ".csv"
        path = base_path + '/' + filename
        path = preprocess(path)

        image_size = 128
        color      = False
        if image_to_csv:
            convert_image(preprocess(base_path) + '/', filename, image_size, color)

        if not os.path.isfile(path):
            raise ValueError("Unrecognized dataset name: " + which_set)

        # If the file name contains a "train", header is True.
        if "train" in which_set:
            X, y = self._load_data(path, True)
        else:
            X, y = self._load_data(path, False)

        if start is not None:
            assert which_set != 'test'
            assert isinstance(start, int)
            assert isinstance(stop, int)
            assert start >= 0
            assert start < stop
            assert stop <= X.shape[0]
            X = X[start:stop, :]
            if y is not None:
                y = y[start:stop, :]

        if color:
            color_shape = 3
        else:
            color_shape = 1

        view_converter = DefaultViewConverter(shape=[image_size, image_size, color_shape], axes=axes)

        super(HogeDataset, self).__init__(X=X, y=y, view_converter=view_converter)

        if preprocessor:
            preprocessor.apply(self, can_fit=fit_preprocessor)

    def adjust_for_viewer(self, X):
        return (X - 127.5) / 127.5

    def get_test_set(self):
        return EmotionsDataset(**self.test_args)

    def _load_data(self, path, expect_labels):

        assert path.endswith('.csv')

        # If a previous call to this method has already converted
        # the data to numpy format, load the numpy directly
        X_path = path[:-4] + '.X.npy'
        Y_path = path[:-4] + '.Y.npy'
        if os.path.exists(X_path):
            X = np.load(X_path)
            if expect_labels:
                y = np.load(Y_path)
            else:
                y = None
            return X, y

        # Convert the .csv file to numpy
        csv_file = open(path, 'r')

        reader = csv.reader(csv_file)

        y_list = []
        X_list = []

        for row in reader:
            if expect_labels:
                y_str     = row[0]
                X_row_str = row[1:]
                y = int(y_str)
                y_list.append(y)
            else:
                X_row_str = row
            X_row_strs = X_row_str
            X_row = map(lambda x: float(x), X_row_str)
            X_list.append(X_row)

        X = np.asarray(X_list).astype('float32')
        if expect_labels:
            y = np.asarray(y_list)

            one_hot = np.zeros((y.shape[0],7),dtype='float32')
            for i in xrange(y.shape[0]):
                one_hot[i,y[i]] = 1.
            y = one_hot
        else:
            y = None

        np.save(X_path, X)
        if y is not None:
            np.save(Y_path, y)

        return X, y
