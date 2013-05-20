# -*- coding: utf-8 -*-
from itertools import repeat
import multiprocessing
from PIL import Image
import numpy
import scipy.fftpack


def bin_to_int(bin_arr):
    """
    Converts binary array to a vector of integers.
    """
    return bin_arr.dot(1 << numpy.arange(bin_arr.shape[-1] - 1, -1, -1))


def int_to_hex(int):
    """
    Converts vector of integers to hex string.
    """
    return "".join([hex(xx)[2:].zfill(2) for xx in int])


def aHash(image, hash_size=8):
    """
    Computes aHash.
    """
    image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
    pixels = numpy.array(image.getdata()).reshape((hash_size, hash_size))
    avg = pixels.mean()
    return pixels > avg



def dHash(image, hash_size=8):
    """
    Computes dHash.
    """
    image = image.convert("L").resize((hash_size + 1, hash_size), Image.ANTIALIAS)
    pixels = numpy.array(image.getdata(), dtype=numpy.float).reshape((hash_size + 1, hash_size))
    return pixels[1:, :] > pixels[:-1, :]


def pHash(image, hash_size=32):
    """
    Computes pHash.
    """
    image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
    pixels = numpy.array(image.getdata(), dtype=numpy.float).reshape((hash_size, hash_size))
    dct = scipy.fftpack.dct(pixels)
    dct_low = dct[:8, 1:9]
    avg = dct_low.mean()
    return dct_low > avg


class Hash(object):
    def __init__(self, params):
        (image_path, hash_function) = params
        self.path = image_path
        self.binary = hash_function(Image.open(image_path))
        self.vec = bin_to_int(self.binary)
        self.hex_str = None

    def __str__(self):
        if not self.hex_str:
            self.hex_str = int_to_hex(self.vec)
        return self.hex_str

    def __eq__(self, other):
        return numpy.array_equal(self.binary, other.binary)

    def __ne__(self, other):
        return not numpy.array_equal(self.binary, other.binary)


def get_hashes(image_paths, hash_function=pHash):
    """
    Returns hashes of all images.
    """
    try:
        cpu_count = multiprocessing.cpu_count()
    except NotImplementedError:
        cpu_count = 2
    pool = multiprocessing.Pool(processes=cpu_count)
    return pool.map(Hash, zip(image_paths, repeat(hash_function)))