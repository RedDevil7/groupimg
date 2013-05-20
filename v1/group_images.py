# -*- coding: utf-8 -*-
import sys
import hcluster
import find_files
import compute_hashes
import time

if __name__ == '__main__' and len(sys.argv) > 1:
    print "searching for images..."
    images = find_files.find_images(sys.argv[1])
    images_length = len(images)
    print images_length, "images found"
    if images_length > 0:
        hash_start_time = time.time()
        print "computing hashes and vectors..."
        hashes = compute_hashes.get_hashes(images)
        hash_end_time = time.time()
        print "all hashes computed in", hash_end_time - hash_start_time
        print "clustering..."
        hcluster.hcluster(hashes)