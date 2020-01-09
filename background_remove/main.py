import os
import os.path

#import matplotlib
#matplotlib.use("PS")

import cv2 as cv
import builder
import effect
from instance import to_bgr

from mrcnn import utils
from mrcnn import model as modellib
from samples.coco import coco


def mrcnn_model_init():
    # Load the pre-trained model data
    ROOT_DIR = os.getcwd()
    MODEL_DIR = os.path.join(ROOT_DIR, "logs")
    COCO_MODEL_PATH = os.path.join(ROOT_DIR, "mask_rcnn_coco.h5")
    if not os.path.exists(COCO_MODEL_PATH):
        utils.download_trained_weights(COCO_MODEL_PATH)

    # Change the config infermation
    class InferenceConfig(coco.CocoConfig):
        GPU_COUNT = 1

        # Number of images to train with on each GPU. A 12GB GPU can typically
        # handle 2 images of 1024x1024px.
        # Adjust based on your GPU memory and image sizes. Use the highest
        # number that your GPU can handle for best performance.
        IMAGES_PER_GPU = 1

    config = InferenceConfig()

    # COCO dataset object names
    model = modellib.MaskRCNN(
        mode="inference", model_dir=MODEL_DIR, config=config
    )
    model.load_weights(COCO_MODEL_PATH, by_name=True)
    return model

def apply_effect(root):
    effectType = input("Please enter the effect type(move/blur/gray/binarization): ")
    if (effectType == "blur"):
        root.setEffect(effect.BlurFilter())
    elif (effectType == "move"):
        amount = input("Please enter the move amount (x, y): ")
        x, y = amount.replace("(", "").replace(")", "").replace(" ", "").split(",")
        root.setEffect(effect.Move((int(x), int(y))))
    elif (effectType == "gray"):
        root.setEffect(effect.GrayEffect())
    elif (effectType == "binarization"):
        thres = input("Binarization threshold: ")
        root.setEffect(effect.Binarization(threshold=int(thres)))
    else:
        print("not such effect")

def save_image(image, output_path = None):
    if output_path is None:
        output_path = input("Please enter the input image path: ")
    output_path = os.path.expanduser(output_path)
    if (output_path.split(".")[-1] != "png"):
        image = to_bgr(image)
    cv.imwrite(output_path, image)

def print_image_hierachy(root):
    for node in root:
        pass

def selectInstance(root):
    className = input("Instance class to apply effect: ")
    for instance in root.find(className):
        apply_effect(instance)

def read_image(filePath = None):
    if filePath is None:
        source_path = input("Please enter the input image path: ")
    else:
        source_path = filePath

    image = cv.imread(os.path.expanduser(source_path), -1)
    if image is None:
        raise Exception("Cannot read image")
    return image

def main():
    model = mrcnn_model_init()
    print("--------model init success--------")

    while True:
        try:
            image = read_image()
            break
        except Exception as e:
            print("Exception: {}".format(e))

    results = model.detect([image], verbose=0)

    instance_builder = builder.Builder()
    root = instance_builder.build(image, results)[0]

    while(True):
        cv.imshow("image", root.generate_image())
        cv.waitKey(1)
        #cv.imwrite("temp.png", root.generate_image())
        instruction = input("Please enter the instruction(effect/save): ")
        if (instruction == "effect"):
            print("All instances detected: ")
            print(root.list())
            selectInstance(root)
        elif(instruction == "save"):
            save_image(root.generate_image())
            break
        else:
            print("not such instruction")

    cv.destroyAllWindows()

def guiMRCNNMain():
    return mrcnn_model_init()
    print("--------model init success--------")

def buildInstanceTree(mrcnnModel, image):
    results = mrcnnModel.detect([image], verbose=0)
    instanceBuilder = builder.Builder()
    return instanceBuilder.build(image, results)[0], results


if __name__ == '__main__':
    main()
