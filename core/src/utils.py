import json
import os
import torch
import random
import xml.etree.ElementTree as ET
import torchvision.transforms.functional as FT
from os import listdir
from os.path import isfile, join

device = torch.device('cpu')

# Labels maps
labels = ('with_mask', 'without_mask')
labels_map = {k: v + 1 for v, k in enumerate(labels)}
labels_map['background'] = 0
rev_label_map = {v: k for k, v in labels_map.items()}
distinct_colors = ['#3cb44b', '#e6194B', '#ffffff']
label_color_map = {k: distinct_colors[i]
                   for i, k in enumerate(labels_map.keys())}

def find_intersection(set_1, set_2):
    lower_bounds = torch.max(set_1[:, :2].unsqueeze(1), set_2[:, :2].unsqueeze(0))
    upper_bounds = torch.min(set_1[:, 2:].unsqueeze(1), set_2[:, 2:].unsqueeze(0))
    intersection_dims = torch.clamp(upper_bounds - lower_bounds, min=0)
    return intersection_dims[:, :, 0] * intersection_dims[:, :, 1]

def find_jaccard_overlap(set_1, set_2): # https://en.wikipedia.org/wiki/Jaccard_index

    # Find intersections
    intersection = find_intersection(set_1, set_2)

    # Find areas of each box in both sets
    areas_set_1 = (set_1[:, 2] - set_1[:, 0]) * (set_1[:, 3] - set_1[:, 1])
    areas_set_2 = (set_2[:, 2] - set_2[:, 0]) * (set_2[:, 3] - set_2[:, 1])

    union = areas_set_1.unsqueeze(1) + areas_set_2.unsqueeze(0) - intersection

    return intersection / union