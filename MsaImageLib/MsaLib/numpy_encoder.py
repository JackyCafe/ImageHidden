'''
MsaImageLib/MsaLib
numpy_encoder.py
ImageHidden
Created by user at 2022/4/23
'''
import json
import numpy as np


class NumpyEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, np.ndarray):
            return obj.tolist()
        return json.JSONEncoder.default(self, obj)