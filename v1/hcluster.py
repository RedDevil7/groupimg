# -*- coding: utf-8 -*-
import scipy.cluster.hierarchy as hier
import scipy.spatial.distance as dist
import fastcluster
import time
import matplotlib.pyplot as plt
import pylab
import numpy as np
from PIL import Image


def hcluster(hashes, metric='euclidean'):
    vectors = [hash.vec for hash in hashes]
    start_distm_time = time.time()
    distanceMatrix = dist.pdist(vectors, metric)
    end_distm_time = time.time()
    distanceSquareMatrix = dist.squareform(distanceMatrix)
    start_link_time = time.time()
    #linkageMatrix = hier.linkage(distanceSquareMatrix)
    linkageMatrix = fastcluster.linkage(distanceSquareMatrix)
    end_link_time = time.time()
    print "distance matrix created in", end_distm_time - start_distm_time
    print "hierarchy found in", end_link_time - start_link_time
    print "creating dendrogram..."
    hier.dendrogram(linkageMatrix)
    plt.savefig("hcluster.png", dpi=600)
    plt.show()