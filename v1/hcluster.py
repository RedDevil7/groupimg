# -*- coding: utf-8 -*-
from numpy import *
from itertools import combinations
from distances import *
from compute_hashes import *
from PIL import Image, ImageDraw

THUMBNAIL_SIZE = 150


class Cluster(object):
    def __init__(self, hash, hex=None, left=None, right=None, id=None, distance=0, path=None):
        self.left = left
        self.right = right
        self.hash = hash
        self.hex = hex
        self.id = id
        self.distance = distance
        self.path = path

    def get_height(self):
        """Returns the height of the tree."""
        if self.path:
            return 1
        return self.left.get_height() + self.right.get_height()

    def get_depth(self):
        """Returns the depth of the tree."""
        if self.path:
            return 0
        return max(self.left.get_depth(), self.right.get_depth()) + self.distance

    def draw(self, draw, x, y, s, graph):
        """Draws the node on a given image."""
        if self.path:
            image = Image.open(self.path)
            image.thumbnail([THUMBNAIL_SIZE, THUMBNAIL_SIZE])
            ns = image.size
            graph.paste(image, [int(x), int(y - ns[1] // 2), int(x + ns[0]), int(y + ns[1] - ns[1] // 2)])
        else:
            h1 = int(self.left.get_height() * THUMBNAIL_SIZE / 2)
            h2 = int(self.right.get_height() * THUMBNAIL_SIZE / 2)
            top = y - (h1 + h2)
            bottom = y + (h1 + h2)

            # vertical line to children
            draw.line((x, top + h1, x, bottom - h2), fill=(0, 0, 0))

            # horizontal lines
            ll = self.distance * s
            draw.line((x, top + h1, x + ll, top + h1), fill=(0, 0, 0))
            draw.line((x, bottom - h2, x + ll, bottom - h2), fill=(0, 0, 0))

            # draw left and right child nodes recursively
            self.left.draw(draw, x + ll, top + h1, s, graph)
            self.right.draw(draw, x + ll, bottom - h2, s, graph)


def avg_hash(cluster1, cluster2):
    """ Averages two hex hashes. """
    hex1 = cluster1.hex
    hex2 = cluster2.hex
    s = []
    for i in xrange(0, len(hex1), 2):
        s.append(hex((int(hex1[i:i + 2], 16) + int(hex2[i:i + 2], 16)) / 2)[2:].zfill(2))
    return "".join(s)


def hcluster(hashes, distance=hamming):
    """Performs hierarchical clustering."""
    dist_cache = {}

    clusters = [Cluster(hash=hash, hex=hex, path=path, id=i) for i, (hash, hex, path) in enumerate(hashes)]

    while len(clusters) > 1:
        best_dist = float('Inf')

        for i, j in combinations(clusters, 2):
            if (i, j) not in dist_cache:
                dist_cache[i, j] = distance(i, j)

            dist = dist_cache[i, j]
            if dist < best_dist:
                best_dist = dist
                closest_nodes = (i, j)
        i, j = closest_nodes

        new_hash = avg_hash(i, j)

        new_cluster = Cluster(hash=hex_to_hash(new_hash), hex=new_hash, left=i, right=j, distance=best_dist)
        clusters.remove(i)
        clusters.remove(j)
        clusters.append(new_cluster)

    return clusters[0]


def draw_dendrogram(node, nodes, filename='hcluster.jpg'):
    """Draws the dendrogram for a given clustering."""
    height = node.get_height() * THUMBNAIL_SIZE
    width = nodes * (THUMBNAIL_SIZE / 2)

    s = float(width - (3 * THUMBNAIL_SIZE)) / node.get_depth()

    graph = Image.new('RGB', (width, height), (255, 255, 255))
    draw = ImageDraw.Draw(graph)

    draw.line((0, height / 2, THUMBNAIL_SIZE, height / 2), fill=(0, 0, 0))

    node.draw(draw, THUMBNAIL_SIZE, (height / 2), s, graph)
    graph.save(filename)
    graph.show()