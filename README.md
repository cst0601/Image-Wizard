# Image Wizard
A tool that allows user to select mutliple items to be segmented by Mask R-CNN and remove the background of the image/video for editing.
This model is from an implementation from [matterporter/Mask_RCNN](https://github.com/matterport/Mask_RCNN) and some code was modified to this application.

Tjis is a copy of the project [ImageWizard](https://gitlab.com/f870103/mask-r-cnn-background-remove)
Credit of the early versions of Image Wizard goes to:
jysh1214, kaze (CK Lai), Chikuma (ST Chien) and scottLiu.

## Release v 1.5
Image Wizard finally have a release!
Note that this only runs on linux distributions (only Ubuntu 18.04 is tested)
See releases to download.

## Build Instructions
1. Install pyinstaller via pip `pip3 install pyinstaller`
2. Build the project by issuing command: `pyinstaller --onefile --paths=background_remove main.py`
3. Image Wizard requrires some dependencies, the file structure should look like:
    - main (the binary file)
    - mask_rcnn_coco.h5
    - gui/
        - image_wizard_main.glade
        - image_wizard_logo/
            - image_wizard.svg

## TODOS:

### Issues:
- **[CRITICAL]**: Think of a better design of Model, Builder, View(Handler)
    - Is multiple Handler(View) acceptable?
    - Does multiple views share a same model? Or sharing model is a bad idea? (Is this against Single responsibility principle?)
### Requirements that needed to be fulfilled:
- [x] Mask RCNN function docking with GUI.
- [x] About window(dialogue)
- [x] Save file
- [x] Edit, redo, undo
- [x] Select instances, need to have indication of the object.
- [x] Resize the image view, show indicator of the resize rate.
- [x] Apply effects to instances.
;)
