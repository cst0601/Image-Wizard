import gi
gi.require_version('Gtk', '3.0')
from gi.repository import Gtk


class Handler:
    def __init__(self,):
        

        window = builder.get_object("window1")
        window.connect("destroy", Gtk.main_quit)

        filepath = builder.get_object("filechooserbutton1")
        print(filepath.get_filename())

        image = builder.get_object("image1")
        image.set_from_file("cat.jpg")
        window.show_all()  # show all widgets

    def onDestroy(self, *args):
        Gtk.main_quit()

    def start_clicked(self, button):
        print("Clicked Start button")


    def save_clicked(self, button):
        print("Clicked Save button")

    def detect_clicked(self, button):
        print("Clicked Detect button")

    def file_set(self, button):
        print("File selected")

    def effect_changed(self, box, selected_button):
        print("Group button changed")
        print(selected_button.get_label())




if __name__ == "__main__":
    builder = Gtk.Builder()
    builder.add_from_file("ImageWizard.glade")
    builder.connect_signals(Handler())

    window = builder.get_object("window1")
    window.show_all()

    Gtk.main()