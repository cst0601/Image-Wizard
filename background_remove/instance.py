import numpy as np
import cv2 as cv

class InitializeException(Exception):
    def __init__(self, class_type):
        self.message = f"Class {class_type} is an interface. Therefore, you cannot create an concrete object of this class."

    def __str__(self):
        return self.message

"""
transparency:   0   -> transparent
                255 -> opaque
"""
def alpha_compositing(foreground, background):
    # refer to https://en.wikipedia.org/wiki/Alpha_compositing
    if foreground.shape != background.shape:
        raise ValueError(f"two images are with different shapes: {foreground.shape} and {background.shape}")
    result = np.full(background.shape, 255, dtype = float)
    result[:,:,3] = 0
    foreground = foreground.astype(float)
    background = background.astype(float)

    foreground[:, :, 3] /= 255
    background[:, :, 3] /= 255

    result[:, :, 3] = foreground[:, :, 3] \
        + np.multiply(background[:, :, 3], np.ones(foreground[:,:,3].shape, dtype=float) - foreground[:,:,3])

    old_setting = np.seterr(divide='ignore', invalid='ignore')
    for i in range(3):
        result[:,:,i] = (np.multiply(foreground[:,:,i], foreground[:,:,3]) \
           + np.multiply(np.multiply(background[:,:,i], background[:,:,3]), np.ones(foreground[:,:,3].shape, dtype=float) - foreground[:,:,3])) \
           / result[:, :, 3]
        result[:,:,i] = np.nan_to_num(result[:,:,i])
    np.seterr(**old_setting)

    result[:, :, 3] *= 255
    return result.astype(np.uint8)

def to_bgr(image):
    result = image[:,:,:3]
    for i in range(3):
        result[:,:,i] = np.multiply(result[:,:,i], image[:,:,3].astype(float) / 255)
    return result

class Node:
    def __init__(self):
        raise InitializeException("Node")

    def init(self):
        self.x = 0
        self.y = 0

    def __len__(self):
        return 0

    def size(self):
        raise NotImplementedError()

    def position(self):
        return (self.x, self.y)

    def add_node(self, instance):
        raise NotImplementedError("Cannot add node under an instance")

    def generate_image(self, image):
        raise NotImplementedError()

    def setEffect(self, effect):
        raise NotImplementedError()

    def getInstanceType (self):
        raise NotImplementedError()

    def list(self):
        raise NotImplementedError()

    def listChild(self):
        raise NotImplementedError()

    def find(self, className):
        raise NotImplementedError()

    def getChildByIndex(self, index):
        raise NotImplementedError()


class Instance(Node):
    # position is left-top position of an image saved as a tuple (x, y)
    def __init__(self, image, class_name, position):
        super().init()
        self.image = image
        self.class_name = class_name
        self.x = position[0]
        self.y = position[1]

    def size(self):
        height, width = self.image.shape[:2]
        return (height + self.y, width + self.x)

    def generate_image(self):
        return self.image

    def setEffect(self, effect):
        # if effect is filter type...
        effect.apply(self)

    def getInstanceType (self):
        return self.class_name

    def list(self):
        return self.getInstanceType()

    def listChild(self):
        return []

    def find(self, className):
        if self.class_name == className:
            return [self]
        return []

class Group(Node):
    def __init__(self):
        super().init()
        self.instances = []

    def __len__(self):
        return len(self.instances)

    def size(self):
        height, width = 0, 0
        for instance in self.instances:
            instance_height, instance_width = instance.size()
            height = instance_height if instance_height > height else height
            width = instance_width if instance_width > width else width
        return (height, width)

    def position(self):
        return (self.x, self.y)

    def add_node(self, instance):
        self.instances.append(instance)

    def generate_image(self):
        # generate bgr image
        result_height, result_width = self.size()
        result = np.zeros((result_height, result_width, 4), dtype = np.uint8)
        if len(self) == 0:
            return result
        for instance in self.instances:
            height, width = instance.size()
            x, y = instance.position()

            region = result[y : height, x : width].astype(float)
            result[y : height, x : width] = alpha_compositing(instance.generate_image(), region)
        return result

    def getInstanceType(self):
        return "Group"

    def list(self):
        result = self.getInstanceType() + "\n"
        for instance in self.instances:
            result += ("\t" + instance.list() + "\n")
        return result

    def listChild(self):
        result = []
        for instance in self.instances:
            result.append(instance)
        return result

    def find(self, className):
        result = []
        if className == self.getInstanceType():
            return [self]
        for instance in self.instances:
            childResult = instance.find(className)
            result.extend(childResult)
        return result

    def setEffect(self, effect):
        for instance in self.instances:
            instance.setEffect(effect)

    def getChildByIndex(self, index):
        return self.instances[index]

    def setChildByIndex(self, index, instance):
        self.instances[index] = instance
