from instance import InitializeException
import cv2 as cv
import numpy as np
import builder

class Effect:
    def __init__(self):
        raise InitializeException("Effect")

    def apply(self, instance):
        raise NotImplementedError()

class Filter(Effect):
    def __init__(self):
        raise InitializeException("Filter")

    def apply(self, instance):
        # border black edge issue
        instance.image = cv.filter2D(instance.image, -1, self.filter)


class UnitFilter(Filter):
    def __init__(self):
        self.filter = np.zeros((3, 3), dtype = np.float32)
        self.filter[1, 1] = 1

class BlurFilter(Filter):
    def __init__(self, filterSize=3):
        self.filter = np.ones((filterSize, filterSize), dtype = np.float32) / (filterSize**2)

class GrayEffect(Effect):
    def __init__(self):
        pass

    def apply(self, instance):
        instance.image[:, :, :3] = cv.cvtColor(cv.cvtColor(instance.image[:, :, :3], cv.COLOR_BGR2GRAY), cv.COLOR_GRAY2BGR)

class Binarization(Effect):
    def __init__(self, threshold):
        self.threshold = threshold

    def apply(self, instance):
        # convert to gray before binarization
        gray = GrayEffect()
        gray.apply(instance)
        sobel = self.sobelEdge(instance)
        _, image = cv.threshold(instance.image[:, :, :3], self.threshold, 255, cv.THRESH_BINARY)
        image = cv.bitwise_and(sobel, image)
        instance.image[:, :, :3] = image

    def sobelEdge(self, instance):
        instance = cv.cvtColor(instance.image[:, :, :3], cv.COLOR_BGR2GRAY)
        sobelX = cv.Sobel(instance, cv.CV_64F, 1, 0)
        sobelY = cv.Sobel(instance, cv.CV_64F, 0, 1)
        sobelX = np.uint8(np.absolute(sobelX))
        sobelY = np.uint8(np.absolute(sobelY))

        sobelCombined = cv.bitwise_or(sobelX, sobelY)
        ret,thresh = cv.threshold(sobelCombined,127,255,cv.THRESH_BINARY_INV)
        thresh = cv.cvtColor(thresh, cv.COLOR_GRAY2BGR)
        return thresh

class Move(Effect):
    def __init__(self, amount):
        self.amount = amount

    def apply(self, instance):
        if instance.x + self.amount[0] < 0 or instance.y + self.amount[1] < 0:
            raise ValueError("Move out to the boundary")
        instance.x += self.amount[0]
        instance.y += self.amount[1]
