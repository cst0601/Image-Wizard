"""
main_window_handler.py
Created by Chikuma, 2019/10/07

Handler of the signals of the main window
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from gui.file_loader import FileLoader
from gui.file_saver import FileSaver
from gui.hint_dialog_controller import HintDialogController, LoadDialogController
from gui.model import Model

# view
class MainWindowHandler:
    def __init__(self, builder):
        self.builder = builder
        self.model = Model()

    def onDestroy (self, userData):
        # TODO: check if the file is saved
        Gtk.main_quit()

    def onOpenClicked (self, userData):
        print("open clicked")
        fileLoader = FileLoader(self.builder.get_object("open_file_chooser"))
        if fileLoader.getFilePath() is not None:
            imagePixbuf = self.model.readImage(fileLoader.getFilePath())
            self.redrawMainImage(imagePixbuf)
            self.resetParams()

    # reset the params of the adjustable view and model params
    def resetParams (self):
        self.builder.get_object("view_percent_label").set_text("100")

    def onSaveClicked (self, userData):
        print("save clicked")
        if self.model.imageSavePath is not None:
            self.model.saveImage()
        else:
            self.onSaveAsClicked(None)

    def onSaveAsClicked (self, userData):
        fileSaver = FileSaver(self.builder.get_object("save_file_chooser"), self.builder.get_object("save_file_name_entry"))
        if fileSaver.getFilePath() is not None:
            self.model.saveImage(fileSaver.getFilePath())

    def onUndoClicked (self, userData):
        self.model.undoEffect()
        self.redrawMainImage(self.model.drawRectOnSelected())

    def onApplyEffectClicked (self, userData):
        print("apply effect")
        try:
            selectedIndex = self.builder.get_object("instance_selection").get_selected_rows()[1][0][0]
        except IndexError:
            HintDialogController(self.builder.get_object("hint_message_dialog"),
                                "Select an instance to apply effect")
            return

        print("proceed the operation...")
        paramVaildFlag = self.model.updateEffectParameters(self.builder.get_object("filter_size_entry").get_text(), self.builder.get_object("threshold_entry").get_text())
        if paramVaildFlag != 0:
            HintDialogController(self.builder.get_object("hint_message_dialog"),
                                "Effect parameter not valid!")
        # if the effect parameters are good...
        if paramVaildFlag == 0:
            loadDialog = LoadDialogController(self.builder.get_object("loading_dialog"))
            loadDialog.start()

            self.model.applyEffect()
            self.redrawMainImage(self.model.drawRectOnSelected())

            loadDialog.hide()

    def showLoadWindow (self):
        self.builder.get_object("loading_dialog").run()

    def onEffectRadioButtonClicked (self, button):
        if button.get_active() is True:
            self.model.setSelectedEffectName(button.get_name())

    def redrawMainImage (self, pixbufImg):
        self.builder.get_object("main_image").set_from_pixbuf(pixbufImg.copy())   # copy prevents the image from corruption?

    def onApplyMaskClicked (self, userData):
        if self.model.isImageLoaded() is True:
            print("apply masking")
            loadDialog = LoadDialogController(self.builder.get_object("loading_dialog"))
            loadDialog.start()

            self.model.applyMasking()

            loadDialog.hide()

            self.loadInstanceTreeView()
        else:
            HintDialogController(self.builder.get_object("hint_message_dialog"),
                                "Image does not exist\nLoad image before applying Mask RCNN")

    # generate gtkListStore and put the data in treeView (or any other kind of views)
    def loadInstanceTreeView (self):
        model = self.model.getInstanceTreeStore()
        self.builder.get_object("instance_tree_view").set_model(model)

    def selectInstance (self, userData):
        selectedRows = self.builder.get_object("instance_selection").get_selected_rows()[1]
        if len(selectedRows) == 0:
            return

        selectedIndex = []
        for index in selectedRows:
            selectedIndex.append(index[0])

        #selectedIndex = selectedRows
        print("The selected index is {}".format(selectedIndex))
        self.model.setSelectedInstanceIndex(selectedIndex)
        self.redrawMainImage(self.model.drawRectOnSelected())

    def onEffectParamChanged (self, *args):
        paramFilter = self.builder.get_object("filter_size_entry")
        paramThres = self.builder.get_object("threshold_entry")
        paramFilter.set_text(''.join([i for i in paramFilter.get_text().strip() if i in '0123456789']))
        paramThres.set_text(''.join([i for i in paramThres.get_text().strip() if i in '0123456789']))

    def onViewResizePlus (self, userData):
        self.model.setViewSizePercent("add")
        self.builder.get_object("view_percent_label").set_text(str(self.model.viewSizePercent))
        self.redrawMainImage(self.model.drawRectOnSelected())

    def onViewResizeMinus (self, userData):
        self.model.setViewSizePercent("minus")
        self.builder.get_object("view_percent_label").set_text(str(self.model.viewSizePercent))
        self.redrawMainImage(self.model.drawRectOnSelected())

    def onAboutClose (self, *args):
        print("about close")
        self.builder.get_object("about_dialog").hide()

    def onAboutClicked (self, userData):
        self.builder.get_object("about_dialog").show_all()
        self.builder.get_object("about_dialog").run()
