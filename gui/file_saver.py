"""
file_saver.py
Created by Chikuma, 2019/10/16
"""
import os
import os.path

import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk

class FileSaver:
    def __init__(self, fileChooserDialog, fileNameEntry):
        self.fileName = None
        self.folderUri = None

        response = fileChooserDialog.run()
        print("saving ...")

        if response == Gtk.ResponseType.OK:
            self.fileName = fileNameEntry.get_text()
            self.folderUri = fileChooserDialog.get_current_folder()
            print("file name = {}".format(self.fileName))
            print("save at: {}".format(fileChooserDialog.get_current_folder()))
        fileChooserDialog.hide()

    def getFilePath (self):
        if self.fileName is None or self.folderUri is None:
            return None
        return self.folderUri + "/" + self.fileName + ".jpg"
