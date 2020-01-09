Image Processing with Machine Learning
===

# Problem Statement
Separating objects and backgrounds is a common operation in editing images and videos, such as depth-of-view, changing/removing image/video backgrounds. However, doing the segmentation of object and background is often tiresome and time consuming. We want to create a program that could easily detect instances on an image and let user could apply different effects.

- Need to save/load images and videos.
- Automatic segmentation of background and foreground objects.
- Create a tree of instances, user could group instances and apply effects.
- Applying different effects/operations on the segmented images and videos.

## Methods used
- [Mask R-CNN](https://arxiv.org/abs/1703.06870)

## Next Steps
- A GUI for users
- Improve efficiency and accuracy of the backbone algorithm.

# Pattern Used
- **Composite**: The tree of instances, user could group instances.
- **Builder**: Create a tree of instances by the information given by Mask R-CNN model(mask, RoI, class id). Instances are cut from the original image by the provided information at this stage.
- **Strategy**: Change the effect to apply on the instance with a uniformed  method.

# Project Members
- 105820049 簡少澤
- 105820023 賴致愷

# Class Diagram
![Diagram](https://i.imgur.com/2gnXdjM.png)

# Force
![Force](https://i.imgur.com/1907adC.png)

# Unit Test
- running all tests by the command `python -m unittest discover -s test -p ut*.py`
- running the specific test by `python -m unittest test.<test_module>`
