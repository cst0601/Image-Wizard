import numpy as np

from instance import Group
from instance import Instance

class Builder:
    def __init__(self, threshold = 0.5):
        self.class_names = [
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
        self.threshold = threshold

    def build(self, image, mask_result):
        result = []
        # check channels to be 4 (b, g, r, alpha)
        height, width, channels = image.shape
        if channels != 4:
            temp = np.full((height, width, 4), 255, dtype = np.uint8)
            temp[:, :, :3] = image
            image = temp

        for mask in mask_result:
            root = Group()
            root.add_node(Instance(image, "background", (0, 0)))
            for i in range(len(mask["class_ids"])):
                if mask["scores"][i] < self.threshold:
                    continue
                top, left, down, right = mask["rois"][i]
                class_name = self.to_class_name(mask["class_ids"][i])
                splitted_image = self.masking(image[top:down, left:right, :], mask["masks"][top:down, left:right, i])
                image[top:down, left:right, :] = self.masking(image[top:down, left:right, :], \
                    np.logical_not(mask["masks"][top:down, left:right, i]))
                root.add_node(Instance(splitted_image, class_name, (left, top)))
            result.append(root)

        return result

    def to_class_name(self, id):
        return self.class_names[id]

    def masking(self, image, mask):
        height, width, channels = image.shape
        result = np.zeros((height, width, 4), dtype = np.uint8)
        for i in range(channels):
            result[:,:,i] = np.multiply(image[:,:,i], mask)
        return result
