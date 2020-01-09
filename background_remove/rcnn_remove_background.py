import cv2 as cv
import numpy as np
import os
import sys
from samples.coco import coco
from mrcnn import utils
from mrcnn import model as modellib
import PIL.Image
import argparse


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
class_names = [
    'BG', 'person', 'bicycle', 'car', 'motorcycle', 'airplane',
    'bus', 'train', 'truck', 'boat', 'traffic light',
    'fire hydrant', 'stop sign', 'parking meter', 'bench', 'bird',
    'cat', 'dog', 'horse', 'sheep', 'cow', 'elephant', 'bear',
    'zebra', 'giraffe', 'backpack', 'umbrella', 'handbag', 'tie',
    'suitcase', 'frisbee', 'skis', 'snowboard', 'sports ball',
    'kite', 'baseball bat', 'baseball glove', 'skateboard',
    'surfboard', 'tennis racket', 'bottle', 'wine glass', 'cup',
    'fork', 'knife', 'spoon', 'bowl', 'banana', 'apple',
    'sandwich', 'orange', 'broccoli', 'carrot', 'hot dog', 'pizza',
    'donut', 'cake', 'chair', 'couch', 'potted plant', 'bed',
    'dining table', 'toilet', 'tv', 'laptop', 'mouse', 'remote',
    'keyboard', 'cell phone', 'microwave', 'oven', 'toaster',
    'sink', 'refrigerator', 'book', 'clock', 'vase', 'scissors',
    'teddy bear', 'hair drier', 'toothbrush'
]


def apply_mask(image, mask):
    if mask is None:
        return image

    image[:, :, 0] = np.where(
        mask == 0,
        125,
        image[:, :, 0]
    )
    image[:, :, 1] = np.where(
        mask == 0,
        12,
        image[:, :, 1]
    )
    image[:, :, 2] = np.where(
        mask == 0,
        15,
        image[:, :, 2]
    )
    return image

def display_instances(image, instances):
    # max_area will save the largest object for all the detection results
    max_area = 0
    mask = None # default

    for object in instances:
        if not np.any(object.roi):
            continue

        # compute the square of each object
        y1, x1, y2, x2 = object.roi
        square = (y2 - y1) * (x2 - x1)

        # use label to select person object from all the 80 classes in COCO dataset
        if object.class_name == 'person':
            # save the largest object in the image as main character
            # other people will be regarded as background
            if square > max_area:
                max_area = square
                mask = object.mask
            else:
                continue
        else:
            continue

        # apply mask for the image
    # by mistake you put apply_mask inside for loop or you can write continue in if also
    image = apply_mask(image, mask)

    return image

def transparent_back(image):
    image = image.convert('RGBA')
    L,H = image.size
    color_0 = image.getpixel((0, 0))
    for h in range(H):
        for l in range(L):
            dot = (l, h)
            color_1 = image.getpixel(dot)
            if color_1 == color_0:
                color_1 = color_1[:-1] + (0,)
                image.putpixel(dot, color_1)

    return image

def display_image (image):
    cv.imshow('Figure 1', image)

# apply mask to a frame
def apply_mask (image):
    height, width, channels = image.shape
    results = model.detect([image], verbose=0)
    r = results[0]
    frame = display_instances(
         image, r['rois'], r['masks'], r['class_ids'], class_names, r['scores']
    )

    return image

def process_video(source_path, output_path, show_frame=False):
    cap = cv.VideoCapture(source_path)
    if not cap.isOpened():
        print("cannot open source.")
        return

    # Video writer attributres
    fps = cap.get(cv.CAP_PROP_FPS)
    width = int(cap.get(cv.CAP_PROP_FRAME_WIDTH))
    height = int(cap.get(cv.CAP_PROP_FRAME_HEIGHT))
    fourcc = cv.VideoWriter_fourcc(*'mp4v')
    writer = cv.VideoWriter()
    writer.open(filename='output_path', fourcc=fourcc, fps=fps, frameSize=(width, height), isColor=True)

    while cap.isOpened() and writer.isOpened():
        # read the video frame by frame, if the frame is read correctly ret == true
        ret, frame = cap.read()
        if not ret:
            print("Can't receive frame (stream end?). exit.")
            break

        image_rm_bg = apply_mask(frame)
        if show_frame:
            display_image(image_rm_bg)
        writer.write(image_rm_bg)

        # exit the program
        if cv.waitKey(1) & 0xFF == ord('q'):
            print('Intrrupted. Exit the process.')
            break

    # release the capture
    cap.release()
    cv.destroyAllWindows()

def process_image(source_path, output_path):
    image = cv.imread(source_path, -1)

    height, width, channels = image.shape
    results = model.detect([image], verbose=0)

    import builder
    import effect
    from instance import to_bgr

    instance_builder = builder.Builder()
    root = instance_builder.build(image, results)[0]
    # root.setEffect(effect.BlurFilter())
    root.setEffect(effect.Move((100, 100)))
    result = root.generate_image()
    cv.imwrite(output_path, result)

    # r = results[0]  # Only one image is inputed

    # DP
    # instances = []
    # import instance
    # for i in range(len(r["rois"])):
    #     instances.append(instance.Instance(r["rois"][i], r["masks"][:, :, i], r["class_ids"][i], class_names[r["class_ids"][i]], r["scores"][i]))

    # for object in instances:
    #     print("Instance Detected: {}".format(object.getInstanceType()))

    # frame = display_instances(image, instances)

    # cv.imwrite('temp.png', image)

    # image = PIL.Image.open("./temp.png")
    # image = transparent_back(image)
    # image.save(output_path)

def process_command():
    parser = argparse.ArgumentParser(prog='Mask R-CNN Image Processor', description=':(')
    parser.add_argument('-s', '--source', type=str, required=True, dest="source_path", help='The path of the source file.')
    parser.add_argument('-o', '--output', type=str, required=True, dest="output_path", help='The path of the output file.')
    parser.add_argument('--show', action="store_true", default=False, help='Show the frame, default is false.')
    group = parser.add_mutually_exclusive_group(required=True)
    group.add_argument('--image', action="store_true", help='Process a image.')
    group.add_argument('--video', action="store_true", help='Process a video.')

    return parser.parse_args()

if __name__ == "__main__":
    args = process_command()
    if args.image:
        process_image(args.source_path, args.output_path)
    elif args.video:
        process_video(args.source_path, args.output_path, args.show)
