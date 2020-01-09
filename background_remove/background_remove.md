# Mask-RCNN-remove-background
Remove background of image by Mask-RCNN.



## Why mask R-CNN?
|               | Center      | Right             |
|:--------------|:-----------:|------------------:|
|Image          |![img](/background_remove/images/biker_original.jpg)     |![img](/background_remove/images/biker_filtered.jpg)           |
|Segmentation   |bounding box |pixel-level mask   |


## Prerequisites
[Mask RCNN](https://github.com/matterport/Mask_RCNN)

## Use
```
python3 rcnn_remove_background.py 1.jpgs
```


## Reference
[Mask R-CNN](https://github.com/matterport/Mask_RCNN)

[Mask-RCNN-remove-background](https://github.com/jysh1214/Mask-RCNN-remove-background)
