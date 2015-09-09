from gi.repository import Gtk, Gdk
import git
import indicator
import settings

class GenericWindow(Gtk.Window):

    def __init__(self, builder_path, object_name, handlers, css_path='../data/styles/commit.css'):
        super().__init__()

        self._create_css_provider(css_path)
        self._init_builder(builder_path, handlers)
        window = self._builder.get_object(object_name) 
        window.show_all()

    def _create_css_provider(self, css_path):
        css_provider = Gtk.CssProvider()
        css_provider.load_from_path(css_path)
        Gtk.StyleContext.add_provider_for_screen(Gdk.Screen.get_default(), css_provider, Gtk.STYLE_PROVIDER_PRIORITY_APPLICATION)
    
    def _init_builder(self, builder_path, handles):
        self._builder = Gtk.Builder()
        self._builder.add_from_file(builder_path)
        self._builder.connect_signals(handles)


class SettingsWindow(GenericWindow):
    BUILDER_PATH = '../data/layouts/settings_window.glade'
    OBJECT_NAME = 'SettingsWindow'
    

    def __init__(self):
        handlers = { 'onSaveClicked': self._save_settings }
    
        super().__init__(self.BUILDER_PATH, self.OBJECT_NAME, handlers)
        self._load_settings()

    def _load_settings(self):
        dir_entry = self._builder.get_object('DirEntry')
        handle_entry = self._builder.get_object('HandleEntry')
        key_entry = self._builder.get_object('KeyEntry')
        pid_entry = self._builder.get_object('PIDEntry')  
  
        data = settings.load_settings() 

        dir_entry.set_text(data['directory'])
        handle_entry.set_text(data['handle'])
        key_entry.set_text(data['key'])
        pid_entry.set_text(data['pid'])

    def _save_settings(self, button):
        dir_entry = self._builder.get_object('DirEntry')
        handle_entry = self._builder.get_object('HandleEntry')
        key_entry = self._builder.get_object('KeyEntry')
        pid_entry = self._builder.get_object('PIDEntry')  
        
        git.set_api_key(dir_entry.get_text(), handle_entry.get_text(), key_entry.get_text())
        git.set_pid(dir_entry.get_text(), pid_entry.get_text())    
        
        settings.save_settings(dir_entry.get_text(), handle_entry.get_text(),\
                               key_entry.get_text(), pid_entry.get_text())

class CommitWindow(GenericWindow):
    BUILDER_PATH = '../data/layouts/commit_window.glade'
    OBJECT_NAME = 'CommitWindow'
   
    def __init__(self, timer_item):
        handlers = { 'onCommitClicked' : self._commit }
        self._timer_item = timer_item 
        super().__init__(self.BUILDER_PATH, self.OBJECT_NAME, handlers)

    def _commit(self, button):
        time_formatted = self._get_time_formatted()
        
        subject_entry = self._builder.get_object('SubjectEntry')
        handles_entry = self._builder.get_object('HandlesEntry')

        git.commit('/home/kuba/Work/Study/University/10_semester/vcs/python-test', \
                   subject_entry.get_text(), time_formatted, handles_entry.get_text())
            
    def _get_time_formatted(self):
        time = self._timer_item.current_time
        self._timer_item.reset_timer()

        minutes, _ = divmod(time, 60)
        hours, minutes = divmod(minutes, 60)

        return "%d h %d min" % (hours, minutes)         


class OverviewWindow(GenericWindow): 
    BUILDER_PATH = '../data/layouts/overview_window.glade'
    OBJECT_NAME = 'OverviewWindow'

    def __init__(self):
        handlers = {'onShaEntered' : self._show_time}
        super().__init__(self.BUILDER_PATH, self.OBJECT_NAME, handlers)

    def _show_time(self):
        commit_label = self._builder.get_object('CommitLabel')
        sha_entry = self._builder.get_object('ShaEntry')
        data = settings.load_settings()
        git_dir = data['directory']
        commit_text = git.show(git_dir, sha_entry.get_text())
        commit_label.set_text(commit_text)
