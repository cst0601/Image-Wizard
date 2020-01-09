"""
    image_hireachy.py
    Created by Neuenmuller, 06/01/2019

    API of managing all nodes(instances and groups) in an image
"""
import instance
import rcnn_remove_background as model

class ImageHierarchy:
    def __init__(self, source_path):
        self.root = model.buildInstances(source_path)
