import unittest
import numpy as np
import cv2 as cv

# add the folder path of "instance" to sys.path
import os
import sys

currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from builder import Builder

class BuilderTest(unittest.TestCase):
    def setUp(self):
        self.image = np.full((300, 400, 4), 255, dtype = np.uint8)
        self.image[:, 190:210, :] = [255, 0, 0, 127]

        height, width, _ = self.image.shape
        mask = np.zeros((height, width, 1), dtype = bool)
        mask[130:180,170:220] = True
        self.mask_result = [{
            "rois": np.array([[130, 170, 180, 220]], dtype = np.int32),
            "class_ids": np.array([0], dtype = np.int32),
            "scores": np.array([0.99], dtype = np.float32),
            "masks": mask
        }]

        self.builder = Builder()

    def test_builder(self):
        result = self.builder.build(self.image.copy(), self.mask_result)[0]
        result_image = result.generate_image()
        result_backgrount = result.instances[0].generate_image()
        result_segment = result.instances[1].generate_image()

        expect_background = np.full((300, 400, 4), 255, dtype = np.uint8)
        expect_background[:, 190:210, :] = [255, 0, 0, 127]
        expect_background[130:180,170:220] = [0, 0, 0, 0]

        segment_image = np.full((50, 50, 4), 255, dtype = np.uint8)
        segment_image[:, 20:40, :] = [255, 0, 0, 127]

        self.assertEqual(2, len(result))
        self.assertEqual((300, 400), result.size())
        self.assertTrue(np.allclose(expect_background, result_backgrount, atol = 5))
        self.assertTrue(np.allclose(segment_image, result_segment, atol = 5))
        self.assertTrue(np.allclose(self.image, result_image, atol = 5))
