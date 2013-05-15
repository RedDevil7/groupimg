# -*- coding: utf-8 -*-
from numpy import *
import Levenshtein


def hamming(cluster1, cluster2):
    """Returns the amount of bits that two clusters differ from each other."""
    return (cluster1.hash != cluster2.hash).sum()


def levenshtein(cluster1, cluster2):
    """Returns Levenshtein distance between two hexes."""
    return Levenshtein.distance(cluster1.hex, cluster2.hex)


def similarity(cluster1, cluster2):
    """Returns distance based on similarity between two hexes."""
    return int((1.0 - Levenshtein.ratio(cluster1.hex, cluster2.hex)) * 100)