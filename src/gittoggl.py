import os
import signal
from gi.repository import Gtk
from gi.repository import AppIndicator3 as AppIndicator
 
APPINDICATOR_ID = 'myAppIndicator'


def app():
    indicator = AppIndicator.Indicator.new(APPINDICATOR_ID, 
        os.path.abspath('sample_icon.svg'), AppIndicator.IndicatorCategory.APPLICATION_STATUS)
    
    indicator.set_status(AppIndicator.IndicatorStatus.ACTIVE)
    indicator.set_menu(popup_menu())
    
    Gtk.main()

def popup_menu(): 
    menu = Gtk.Menu() 
 
    item_about = Gtk.MenuItem(label="00:00 Start") 
    menu.append(item_about) 
    
    item_quit = Gtk.MenuItem(label="Commit") 
    menu.append(item_quit)
     
    item_overview = Gtk.MenuItem(label="Overview") 
    menu.append(item_overview)
    
    item_pref = Gtk.MenuItem(label="Preferences") 
    menu.append(item_pref) 
    
    menu.show_all() 
 
    return menu
 
if __name__ == "__main__":
    signal.signal(signal.SIGINT, signal.SIG_DFL)
    app()
