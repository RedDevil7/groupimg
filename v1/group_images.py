# -*- coding: utf-8 -*-
import sys
import hcluster
import find_files
import compute_hashes


if __name__ == '__main__' and len(sys.argv) > 1:
    images = find_files.find_images(sys.argv[1])
    hashes = compute_hashes.get_hashes(images)
    clustering = hcluster.hcluster(hashes)
    hcluster.draw_dendrogram(clustering, len(hashes))