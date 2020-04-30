import area_detector_handlers
import os
from PIL import Image
import fabio
import numpy as np


class JPEGHandler(area_detector_handlers.HandlerBase):
    specs = {"JPEG"} | area_detector_handlers.HandlerBase.specs

    def __init__(self, path):
        self._file_name = path

    def __call__(self):
        im = Image.open(self._file_name)
        return np.asarray(im)


class TIFFHandler(area_detector_handlers.HandlerBase):
    specs = {"TIFF"} | area_detector_handlers.HandlerBase.specs

    def __init__(self, path):
        self._file_name = path

    def __call__(self):
        im = Image.open(self._file_name)
        return np.asarray(im)


class EDFHandler(area_detector_handlers.HandlerBase):
    specs = {"EDF"} | area_detector_handlers.HandlerBase.specs

    def __init__(self, path):
        self._file_name = path

    def __call__(self):
        im = fabio.open(self._file_name)
        return np.array(im.data)
