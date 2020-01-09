"""
file_loader.py
Created by Chikuma, 2019/09/23
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
"""
class FileLoader
Handle the file chooser dialog and get the file.
"""
class FileLoader:
    def __init__(self, fileChooserDialog):
        self._filename = None
        response = fileChooserDialog.run()
        if response == Gtk.ResponseType.OK:
            self._filename = fileChooserDialog.get_filename()
        print("Open file: {}".format(self._filename))
        fileChooserDialog.hide()

    # do not call this function if opening images
    def getFileContext(self):
        file = open(self._filename, "r")
        return file.read()

    def getFilePath(self):
        return self._filename
