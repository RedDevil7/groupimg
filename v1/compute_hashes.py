# -*- coding: utf-8 -*-
import Image, numpy


def binary_array_to_hex(bin_arr):
    """ Converts binary array to hex string. """
    h = 0
    s = []
    for i, v in enumerate(bin_arr):
        if v:
            h += 2 ** (i & 7)
        if (i & 7) == 7:
            s.append(hex(h)[2:].zfill(2))
            h = 0
    return "".join(s)


def hex_to_hash(hex_str):
    """ Converts hex string to hash(binary array). """
    l = []
    for i in xrange(0, len(hex_str), 2):
        h = hex_str[i:i + 2]
        v = int(h, 16)
        for j in xrange(8):
            l.append(v & 2 ** j > 0)
    return numpy.array(l)


def aHash(image, hash_size=8):
    """ Computes aHash. """
    image = image.convert("L").resize((hash_size, hash_size), Image.ANTIALIAS)
    pixels = numpy.array(image.getdata()).reshape((hash_size, hash_size))
    avg = pixels.mean()
    diff = pixels > avg
    return diff.flatten()


def dHash(image, hash_size=8):
    """ Computes dHash. """
    image = image.convert("L").resize((hash_size + 1, hash_size), Image.ANTIALIAS)
    pixels = numpy.array(image.getdata(), dtype=numpy.float).reshape((hash_size + 1, hash_size))
    diff = pixels[1:, :] > pixels[:-1, :]
    return diff.flatten()


def get_hash(image_path, hash_function=aHash):
    """ Returns hash, hex and path of a given image. """
    image_hash = hash_function(Image.open(image_path))
    return (image_hash, binary_array_to_hex(image_hash), image_path)


def get_hashes(images, hash_function=aHash):
    """ Returns hashes of all images. """
    return [get_hash(image, hash_function) for image in images]