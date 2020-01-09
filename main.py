import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk
from threading import Thread
# a dirty way to load mrcnn models, but it works
import sys
sys.path.append("background_remove")

# handlers
from gui.main_window_handler import MainWindowHandler

# initialize the window program and load mrcnn model
class WindowInitializer:
    def __init__(self):
        self.builder = Gtk.Builder()
        self.builder.add_from_file("gui/image_wizard_main.glade")

        self.initWindow = self.builder.get_object("initialize_window")
        self.window = self.builder.get_object("main_window")

        #splash = SplashWindow(self.initWindow)
        #splash.start()

        # This consumes some time
        self.builder.connect_signals(MainWindowHandler(self.builder))
        print("Done! closing splash window and start main...")

        #splash.destroy()

    def run(self):
        self.window.show_all()
        Gtk.main()

class SplashWindow(Thread):
    def __init__ (self, window):
        super(SplashWindow, self).__init__()
        self.window = window
        self.window.connect("destroy", Gtk.main_quit)

    def run (self):
        self.window.set_auto_startup_notification(False)
        self.window.show_all()
        self.window.set_auto_startup_notification(True)
        Gtk.main()

    def destroy (self):
        self.window.destroy()

if __name__ == "__main__":
    mainWindow = WindowInitializer()
    mainWindow.run()
