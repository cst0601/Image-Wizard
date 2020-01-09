import unittest
import cv2 as cv
import numpy as np

class OpencvTest(unittest.TestCase):
    def setUp(self):
        self.png_image = cv.imread("test/test_images/1_output.png", cv.IMREAD_UNCHANGED)
        self.jpg_image = cv.imread("test/test_images/1.jpg", cv.IMREAD_UNCHANGED)
        self.image_array = np.zeros((300, 400 , 4), dtype=np.uint8)
        self.image_array[:, 180:220, :] = [255, 0, 0, 255]     # blue '1'

    def tearDown(self):
        pass

    def test_png_image(self):
        self.assertIsInstance(self.png_image, np.ndarray)
        self.assertEqual(4, self.png_image.shape[2])
        self.assertEqual(self.png_image.dtype, np.uint8)
        # cv.imshow("png image", self.png_image)
        # cv.waitKey(0)

    def test_jpg_image(self):
        self.assertIsInstance(self.jpg_image, np.ndarray)
        # jpg image format does not have transparency
        self.assertEqual(3, self.jpg_image.shape[2])
        self.assertEqual(self.jpg_image.dtype, np.uint8)
        # cv.imshow("jpg image", self.jpg_image)
        # cv.waitKey(0)

    def test_array(self):
        # cv.imshow("image_array", self.image_array)
        # cv.waitKey(0)
        pass

    def test_filter2D(self):
        kernel = np.ones((5,5),np.float32) / 25
        result = cv.filter2D(self.image_array, -1, kernel)

        # print(self.image_array[:, 180:220, :])
        # print(result[:, 180:220, :])
        # cv.imshow("origin", self.image_array)
        # cv.waitKey(0)
        # cv.imshow("result", result)
        # cv.waitKey(0)

    def test_grayscale(self):
        self.image_array[:, :,:3] = cv.cvtColor(cv.cvtColor(self.image_array, cv.COLOR_BGR2GRAY), cv.COLOR_GRAY2BGR)
        # cv.imshow("origin", self.image_array)
        # cv.waitKey(0)
    


if __name__ == '__main__':
    unittest.main()