import unittest
import cv2 as cv
import numpy as np

# add the folder path of "instance" to sys.path
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from instance import *

class InstanceTest(unittest.TestCase):
    def setUp(self):
        self.root = Group()

        # create a image(300 * 400) with a blue number '1'
        image = np.zeros((300, 40, 4), dtype = np.uint8)
        image[:, :, :] = [255, 0, 0, 127]
        self.instance = Instance(image, "number", (180, 0))

        # create a image(300 * 400) with a blue symbol '-'
        image = np.zeros((40, 400, 4), dtype = np.uint8)
        image[:, :, :] = [0, 255, 0, 127]
        self.another = Instance(image, "symbol", (0, 130))

    def tearDown(self):
        pass

    def test_init_exception(self):
        with self.assertRaises(InitializeException):
            Node()

    def test_len(self):
        self.assertEqual(0, len(self.root))
        self.assertEqual(0, len(self.instance))

    def test_size(self):
        self.assertEqual((0, 0), self.root.size())
        self.assertEqual((300, 220), self.instance.size())

    def test_add_node(self):
        with self.assertRaises(NotImplementedError):
            self.instance.add_node(self.instance)

        self.root.add_node(self.instance)
        self.assertEqual(1, len(self.root))
        self.assertEqual((300, 220), self.root.size())

        self.root.add_node(self.another)
        self.assertEqual(2, len(self.root))
        self.assertEqual((300, 400), self.root.size())

    def test_alpha_compositing(self):
        image = alpha_compositing(self.instance.image, self.instance.image)
        self.instance.image[:, :, 3] = 255*0.5 + 255*0.5*0.5
        self.assertTrue(np.allclose(self.instance.image, image, atol = 5))

    def test_generate_image(self):
        self.root.add_node(self.instance)
        self.root.add_node(self.another)
        image = self.root.generate_image()

        expect = np.zeros((300, 400, 4), dtype = np.uint8)
        expect[:, 180:220, :] = [255, 0, 0, 127]
        expect[130:170, :, :] = [0, 255, 0, 127]
        # alpha = 0.5 + 0.5 * (1-0.5) = 0.75 = 191
        # ((255, 0, 0) * 0.5 + (0, 255, 0) * 0.5 * 0.5) / 0.75 = (85, 170, 0)
        expect[130:170, 180:220, :] = [85, 170, 0, 191]

        self.assertTrue(np.allclose(expect, image, atol = 5))
        # cv.imshow("image_array", to_bgr(image))
        # cv.waitKey(0)

    def test_to_bgr(self):
        expect = np.zeros((300, 40, 3), dtype = np.uint8)
        expect[:, :, :] = [127, 0, 0]

        self.assertTrue(np.allclose(expect, to_bgr(self.instance.image), atol = 5))


if __name__ == '__main__':
    unittest.main()
