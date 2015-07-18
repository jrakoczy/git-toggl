import os
import signal
from gi.repository import Gtk, GLib
from gi.repository import AppIndicator3 as AppIndicator
 
APPINDICATOR_ID = 'myAppIndicator'


def app():
    indicator = AppIndicator.Indicator.new(APPINDICATOR_ID, 
        os.path.abspath('sample_icon.svg'), AppIndicator.IndicatorCategory.APPLICATION_STATUS)
    
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(popup_menu())
    
    Gtk.main()

def update_timer_label(item_timer):
    current_time = int(item_timer.get_label())
    item_timer.set_label(str(current_time + 1))
    return True

def popup_menu(): 
    menu = Gtk.Menu() 
 
    item_timer = Gtk.MenuItem(label="0") 
    menu.append(item_timer) 

    GLib.timeout_add(1000, update_timer_label, item_timer)
    
    item_commit = Gtk.MenuItem(label="Commit") 
    menu.append(item_commit)
     
    item_overview = Gtk.MenuItem(label="Overview") 
    menu.append(item_overview)
    
    item_pref = Gtk.MenuItem(label="Preferences") 
    menu.append(item_pref) 
    
    menu.show_all() 
 
    return menu


 
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app()
