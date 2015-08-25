import os
import signal
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as AppIndicator
from windows import CommitWindow
from windows import SettingsWindow
 
APPINDICATOR_ID = 'GittogglIndicator'


def run_application():
    indicator = AppIndicator.Indicator.new(APPINDICATOR_ID, 
        os.path.abspath('sample_icon.svg'), AppIndicator.IndicatorCategory.APPLICATION_STATUS)
    
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(IndicatorMenu())
    
    Gtk.main()


class IndicatorMenu(Gtk.Menu): 
    COMMIT_LABEL_TEXT = 'Commit'
    SETTINGS_LABEL_TEXT = 'Settings'
    OVERVIEW_LABEL_TEXT = 'Overview'
    QUIT_LABEL_TEXT = 'Quit'

    def __init__(self):
        super().__init__()
        self._build_indicator_menu()
        self.show_all()
        
    def _build_indicator_menu(self):
        self.append(TimerMenuItem())        

        commit_item = Gtk.MenuItem(label=self.COMMIT_LABEL_TEXT)
        commit_item.connect('activate', self._open_commit_window)
        self.append(commit_item)

        settings_item = Gtk.MenuItem(label=self.SETTINGS_LABEL_TEXT)
        settings_item.connect('activate', self._open_settings_window)
        self.append(settings_item)

        overview_item = Gtk.MenuItem(label=self.OVERVIEW_LABEL_TEXT)
        overview_item.connect('activate', self._open_overview_window)
        self.append(overview_item)

        quit_item = Gtk.MenuItem(label=self.QUIT_LABEL_TEXT)
        quit_item.connect('activate', lambda i: Gtk.main_quit())
        self.append(quit_item)

    def _open_commit_window(self, item):
        CommitWindow()

    def _open_settings_window(self, item):
        SettingsWindow()

    def _open_overview_window(self, item):
        pass



class TimerMenuItem(Gtk.MenuItem):
    UPDATE_PERIOD = 1000 #ms
    PLAY_SYMBOL = u'\u25b6'
    PAUSE_SYMBOL = u'\u25ae' + u'\u25ae'
 
    def __init__(self):
        super().__init__()
        self._timer = None
        self.reset_timer() 
        self.connect('activate', self._switch_timer_state)
    
    def reset_timer(self):
        self._current_time = 0  
        self._stop_timer()
        

    def _switch_timer_state(self, item):
        if self._is_ticking:
            self._stop_timer()
        else:
            self._start_timer()
            
    def _start_timer(self):
        self._is_ticking = True
        self._update_timer_label()
        self._timer = GLib.timeout_add(self.UPDATE_PERIOD, self._tick)
        
    def _stop_timer(self):
        
        if self._timer is not None:
            GLib.source_remove(self._timer)

        self._is_ticking = False
        self._update_timer_label()
        
    def _tick(self):
        self._current_time += 1
        self._update_timer_label()
        
        return True

    def _update_timer_label(self): 
        minutes, seconds = divmod(self._current_time, 60)
        hours, minutes = divmod(minutes, 60)
        time_label = '%d:%02d:%02d ' % (hours, minutes, seconds)
       
        current_symbol = self.PAUSE_SYMBOL if self._is_ticking else self.PLAY_SYMBOL

        self.set_label(time_label + current_symbol) #Gtk handles unicode encoding
   
