from gi.repository import Gtk, Gdk

class GenericWindow(Gtk.Window):

    def __init__(self, builder_filename, object_name, css_path='commit.css'):
        super().__init__()

        self._create_css_provider(css_path)
        window = self._build_window(builder_filename, object_name)        
        window.show_all()

    def _create_css_provider(self, css_path):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(css_path)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    
    def _build_window(self, builder_filename, object_name):
        builder = Gtk.Builder()
        builder.add_from_file(builder_filename)
        return builder.get_object(object_name)


class SettingsWindow(GenericWindow):
    BUILDER_FILENAME = 'settings_window.glade'
    OBJECT_NAME = 'CommitWindow'

    def __init__(self):
        super().__init__(self.BUILDER_FILENAME, self.OBJECT_NAME)


class CommitWindow(GenericWindow):
    BUILDER_FILENAME = 'commit_window.glade'
    OBJECT_NAME = 'CommitWindow'

    def __init__(self):
        super().__init__(self.BUILDER_FILENAME, self.OBJECT_NAME)

