import logging
from logging.handlers import SysLogHandler
import gtk
import BCTimer
import os
import sys

class App:
    ROOTDIR = os.path.join(os.path.abspath(os.path.dirname(sys.argv[0])))
    
    def __init__(self):
        self.setup_logger()
        self.setup_menu()
        
    def setup_logger(self):
        logging.basicConfig(level=logging.DEBUG)
        syslog = SysLogHandler(address='/dev/log')
        self.logger = logging.getLogger()
        self.logger.addHandler(syslog)
        
    def setup_menu(self):
        builder = gtk.Builder()
        builder.add_from_file(App.ROOTDIR + '/' + "actions_menu.glade") 
        self.menu = builder.get_object("menuActions")
        
        #~ entry_time = builder.get_object("entryTime")
        #~ entry_time.modify_text(gtk.STATE_NORMAL, gtk.gdk.color_parse("red")) 
        #~ 
        #~ size = 22.0
        #~ style = entry_time.style
        #~ font_desc = style.font_desc.copy()
        #~ font_desc.set_size(28)
        #~ entry_time.modify_font(pango.FontDescription('courier Medium 32'))
        #~ 
        #~ self.entry_time = entry_time
        
        #~ context = entry_time.get_pango_context()
        #~ font = context.get_font_description()
        #~ font.set_size(int(font.get_size() * 4))
        #~ entry_time.modify_font(font)
        #~ 
        #~ print font.__class__
        #~ 
        #~ gtk.rc_parse_string("""
            #~ style "entryTime_style"
            #~ {
                #~ font_name="Sans Serif 24"
            #~ }
            #~ class "GtkEntry" style "entryTime_style"
        #~ """);
        
        actions_menu = ActionsMenu(self)
        builder.connect_signals(actions_menu)
        
        self.app_indicator = BCTimer.plugins.AppIndicatorMenu(self.menu)

class ActionsMenu(gtk.Menu):
    def __init__(self, app):
        self.app = app
    
    #When the applet is clicked
    #~ def on_menuActions_button_press_event(self, button, event):
        #~ self.app.logger.debug('button_press')
#~ 
        #~ # left mouse button
        #~ if event.button == 1:
            #~ self.left_click(event)
            #~ 
        #~ # scroll wheel mouse button
        #~ elif event.button == 2:
            #~ pass
#~ 
        #~ # right mouse button
        #~ elif event.button == 3:
            #~ self.right_click(event)
            #~ button.emit_stop_by_name("button_press_event") #else the menu doesn't show
            #~ 
    #~ def left_click(self, event):
        #~ self.app.logger.debug('left_click')
        #~ #self.butxton.set_relief(gtk.RELIEF_NORMAL)
        #~ #self.show_leftclick_menu(event)
        #~ #self.menu().popup(None, None, self.menu_position, event.button, event.time)
        #~ return True
        
    def right_click(self, event):
        self.app.logger.debug('right_click')
    
    def on_menuitemStartTimer_activate(self, event):
        self.app.logger.debug('on_menuitemStartTimer_activate')
    
    def on_menuitemResetTimer_activate(self, event):
        self.app.logger.debug('on_menuitemResetTimer_activate')
        
    def on_menuitemShowTimer_activate(self, event):
        self.app.logger.debug('on_menuitemShowTimer_activate')
        #self.app.logger.debug(BCTimer.windows.Timer.getInstance())
        BCTimer.windows.Timer.getInstance(self.app).show()
        
    def on_menuitemEditTimer_activate(self, event):
        self.app.logger.debug('on_menuitemEditTimer_activate')
        
    def on_menuitemRoundTime_activate(self, event):
        self.app.logger.debug('on_menuitemRoundTime_activate')
        
    def on_menuitemProjects_activate(self, event):
        self.app.logger.debug('on_menuitemProjects_activate')
        
    def on_menuitemIntegration_activate(self, event):
        self.app.logger.debug('on_menuitemIntegration_activate')
