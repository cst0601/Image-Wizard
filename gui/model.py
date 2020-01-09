"""
model.py
Created by Chikuma, 2019/10/06
"""
import numpy as np
import cv2 as cv
import copy

import background_remove.main as br
import background_remove.builder as builder
import background_remove.effect as effect
import new_blur_effect as newBlurEffect
# for converting openCV images to GtkImage for display
from gi.repository import GdkPixbuf
from gi.repository import Gtk # <--- only using treeStore here, does not violate MVC :)

class Model:
    def __init__(self):
        self.mrcnn = br.guiMRCNNMain()
        self.image = None
        self.root = None
        self.undoRoot = None
        self.maskResults = None
        self.selectedEffectName = "blur"
        self.imagePath = None
        self.imageModified = False
        self.imageSavePath = None
        self.filterSize = 3
        self.binarizationThreshold = 50
        self.viewSizePercent = 100
        self.selectedInstIndex = None

    def readImage (self, filePath):
        self.undoRoot = None

        self.image = br.read_image(filePath)
        self.imagePath = filePath
        self.imageModified = False
        self.imageSavePath = None
        self.viewSizePercent = 100
        return self.imageToGdkPixBuf(self.image.copy())

    def undoEffect (self):
        self.root = self.undoRoot
        self.image = self.root.generate_image()

    # convert openCV image to GdkPixbuf image for GTKImage display
    def imageToGdkPixBuf(self, openCvImage):
        height, width, d = openCvImage.shape
        openCvImage = cv.cvtColor(openCvImage, cv.COLOR_BGR2RGB)
        openCvImage = np.array(openCvImage, dtype=np.uint8).ravel()
        pixbuf = GdkPixbuf.Pixbuf.new_from_data(openCvImage, GdkPixbuf.Colorspace.RGB, False, 8, width, height, width*3)
        return pixbuf

    # apply mask to image, build up the instance tree
    # returns nothing, get the instance list by getInstanceList()
    def applyMasking (self):
        self.root, self.maskResults = br.buildInstanceTree(self.mrcnn, self.image)
        self.undoRoot = copy.deepcopy(self.root)

    def getInstanceTreeStore (self):
        self.listStore = Gtk.ListStore(str)
        for instance in self.root.listChild():
            print(instance.getInstanceType())
            self.listStore.append([instance.getInstanceType()])

        return self.listStore

    def setSelectedInstanceIndex (self, instIndex):
        self.selectedInstIndex = instIndex

    def resizeByPercentage(self, image):
        height, width = image.shape[:2]
        width = int(width * self.viewSizePercent / 100)
        height = int(height * self.viewSizePercent / 100)
        return cv.resize(image, (width, height))

    # Generate image with instance indicator (a rectangle box), does not effect image in model
    def drawRectOnSelected (self):
        image = self.image.copy()

        if len(self.selectedInstIndex) != 0:
            for index in self.selectedInstIndex:
                selectedInstance = self.root.getChildByIndex(index)
                topLeftXY = selectedInstance.position() # get the top left and botton right for rect drawing
                bottomRightXY = selectedInstance.size()
                cv.rectangle(image, topLeftXY, bottomRightXY, (0, 255, 0), 3)
        image = self.resizeByPercentage(image)

        return self.imageToGdkPixBuf(image)

    def isImageLoaded (self):
        if self.image is None:
            return False
        else:
            return True

    def setSelectedEffectName (self, effectName):
        self.selectedEffectName = effectName
        print("Effect changed to {}".format(effectName))

    def applyEffect (self):
        self.undoRoot = copy.deepcopy(self.root)

        for index in self.selectedInstIndex:
            selectedInstance = self.root.getChildByIndex(index)
            if (self.selectedEffectName == "blur"):
                #selectedInstance.setEffect(effect.BlurEffect())    # original method
                self.root.setChildByIndex(index, newBlurEffect.blurEffect(self.root.generate_image(), self.maskResults, index, self.filterSize))
            elif (self.selectedEffectName == "gray"):
                selectedInstance.setEffect(effect.GrayEffect())
            elif (self.selectedEffectName == "binarization"):
                selectedInstance.setEffect(effect.Binarization(threshold=self.binarizationThreshold))
            else:
                print("not such effect")
        self.imageModified = True
        self.updateImage()

    def isImageModified (self):
        return self.imageModified

    def saveImage (self, filePath = None):
        if filePath is not None:
            self.imageSavePath = filePath
        print (self.imageSavePath)
        br.save_image(self.root.generate_image(), self.imageSavePath)

    def updateImage (self):
        self.image = self.root.generate_image()

    # A very old C style function
    # returns 1 if filter size is illegal
    #         2 if binarization threshold is illegal
    #         0 if everything is good :)
    def updateEffectParameters (self, filterSize, threshold):
        filterSize = int(filterSize)
        threshold = int(threshold)
        if filterSize >= 3 and filterSize <= 300:
            self.filterSize = filterSize
        else:
            return 1
        if threshold > 0 and threshold < 256:
            self.binarizationThreshold = threshold
        else:
            return 2
        return 0

    def setViewSizePercent (self, mode):
        if mode is "add" and self.viewSizePercent < 1000:
            self.viewSizePercent += 10
        elif mode is "minus" and self.viewSizePercent > 10:
            self.viewSizePercent -= 10
