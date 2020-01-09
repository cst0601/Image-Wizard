import unittest

# add the folder path of "instance" to sys.path
import os
import sys
currentdir = os.path.dirname(os.path.realpath(__file__))
parentdir = os.path.dirname(currentdir)
sys.path.append(parentdir)

from instance import *
from effect import *

class EffectTest(unittest.TestCase):
    def setUp(self):
        self.root = Group()

        # create a image(300 * 400) with a blue number '1'
        image = np.zeros((300, 60, 4), dtype = np.uint8)
        image[:, 20:40, :] = [255, 0, 0, 127]
        self.root.add_node(Instance(image, "number", (170, 0)))

        # create a image(300 * 400) with a blue symbol '-'
        image = np.zeros((60, 400, 4), dtype = np.uint8)
        image[20:40, :, :] = [0, 255, 0, 127]
        self.root.add_node(Instance(image, "symbol", (0, 120)))


    def test_UnitFilter(self): 
        filter = UnitFilter()
        expect = self.root.generate_image()
        self.root.setEffect(filter)

        self.assertTrue(np.allclose(expect, self.root.generate_image(), atol = 5))
        # cv.imshow("image_array", self.root.generate_image())
        # cv.waitKey(0)

    def test_BlurFilter(self):
        filter = BlurFilter()

        # calculate expect value
        expect_root = Group()
        kernel = np.ones((3,3),np.float32) / 9

        image = np.zeros((300, 60, 4), dtype = np.uint8)
        image[:, 20:40, :] = [255, 0, 0, 127]
        expect_root.add_node(Instance(cv.filter2D(image, -1, kernel), "number", (170, 0)))

        image = np.zeros((60, 400, 4), dtype = np.uint8)
        image[20:40, :, :] = [0, 255, 0, 127]
        expect_root.add_node(Instance(cv.filter2D(image, -1, kernel), "symbol", (0, 120)))

        expect = expect_root.generate_image()

        self.root.setEffect(filter)
        result = self.root.generate_image()

        self.assertTrue(np.allclose(expect, result, atol = 5))
        # cv.imshow("expect", expect)
        # cv.waitKey(0)
        # cv.imshow("result", result)
        # cv.waitKey(0)
        # np.set_printoptions(threshold=sys.maxsize)
        # print(result-expect)

    def test_gray(self):
        self.root.setEffect(GrayEffect())
        # cv.imshow("Gray", self.root.generate_image())
        # cv.waitKey(0)

    def test_binarization(self):
        self.root.setEffect(GrayEffect())
        self.root.setEffect(Binarization(127))
        # cv.imshow("Binarization", self.root.generate_image())
        # cv.waitKey(0)

    def test_move(self):
        effect = Move((10, 10))

        expect = np.zeros((310, 410, 4), dtype = np.uint8)
        expect[10:, 200:220, :] = [255, 0, 0, 127]
        expect[150:170, 10:, :] = [0, 255, 0, 127]
        expect[150:170, 200:220, :] = [85, 170, 0, 191]

        self.root.setEffect(effect)
        result = self.root.generate_image()

        self.assertEqual((310, 410), self.root.size())
        self.assertTrue(np.allclose(expect, result, atol = 5))

if __name__ == '__main__':
    unittest.main()
