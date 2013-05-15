# -*- coding: utf-8 -*-
import os, sys


def find_images(path=".", image_exts=(".gif", ".jpg", ".jpeg", ".png")):
    """Returns all files that names end with a given extension."""
    return [os.path.join(root, name)
            for root, dirs, files in os.walk(path)
            for name in files
            if name.lower().endswith(image_exts)]


if __name__ == '__main__' and len(sys.argv) > 1:
    print find_images(sys.argv[1])