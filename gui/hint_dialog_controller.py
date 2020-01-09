"""
hint_dialog_controller.py
Created by Chikuma, 2019/10/07

Control the hint dialog
"""
import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from threading import Thread

class HintDialogController:
    def __init__(self, hintDialog, subText):
        hintDialog.format_secondary_text(subText)

        response = hintDialog.run()
        if response == Gtk.ResponseType.OK:
            hintDialog.hide()

class LoadDialogController(Thread):
    def __init__(self, loadDialog):
        super(LoadDialogController, self).__init__()
        self.loadDialog = loadDialog

    def run (self):
        self.loadDialog.show_all()
        self.loadDialog.run()

    def hide (self):
        print("hide?")
        self.loadDialog.hide()
