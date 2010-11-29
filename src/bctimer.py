#!/usr/bin/env python

__author__= "Leon Bogaert"
__email__ = "leon@tim-online.nl"
__date__ = "$Nov 27, 2010 11:37:38 AM$"

import pygtk
pygtk.require('2.0')

import gtk
import gnome
import gnomeapplet
import gobject
import sys
import logging
from logging.handlers import SysLogHandler

class BaseCampTimer_Applet():
    title = 'Basecamp Timer'
    version = '0.0.1'
    icon_name = 'network-offline'

    logging.basicConfig(level=logging.DEBUG)
    syslog = SysLogHandler(address='/dev/log')
    logger = logging.getLogger()
    logger.addHandler(syslog)

    def __init__(self, applet, iid):
        logging.debug('__init__')
        # initializate the gnome internals
        gnome.init("sample", "1.0")

        # save the applet object
        self.applet = applet

        # set up the applet tooltip
        self.applet.set_tooltip_text(self.title)
        
        gtk.rc_parse_string("""
            style "event_box_style"
            {
                GtkWidget::focus-line-width=0
                GtkWidget::focus-padding=0
            }
            style "menu_bar_style"
            {
                ythickness = 0
                GtkMenuBar::shadow-type = none
                GtkMenuBar::internal-padding = 0
            }
            class "GtkEventBox" style "event_box_style"
            class "GtkMenuBar" style:highest "menu_bar_style"
        """);
        
        self.menu_bar = gtk.MenuBar()
        self.menu_item = gtk.MenuItem('00:13')
        
        print self.menu_bar.style_get_property("shadow-type")
        
        #self.menu_bar.set_relief(gtk.RELIEF_NONE)
        #self.menu_bar.state = gtk.STATE_INSENSITIVE
        self.menu_item.set_submenu(self.menu())
        self.menu_bar.append(self.menu_item)
        
        #self.button = gtk.Label()
        #self.button.set_label('asasasd')
        
        #self.button = PanelButton()
        #self.button.connect('toggled', self.on_toggle)
        
        print self.menu_bar.style_get_property('focus-line-width')
        print self.menu_item.style_get_property('focus-line-width')
        
        #self.menu_bar.unset_flags(gtk.CAN_FOCUS)
        
        self.menu_bar.connect('button-press-event', self.button_press)
        #self.applet.connect('change-size', self.change_size, image)
        #self.applet.connect('change-background', self.change_background)
        
        self.applet.add(self.menu_bar)
        
        self.setup_rightclick_menu()

    def left_click(self, event):
        logging.debug('left_click')
        #self.button.set_relief(gtk.RELIEF_NORMAL)
        #self.show_leftclick_menu(event)
        #self.menu().popup(None, None, self.menu_position, event.button, event.time)
        return True
        
    def right_click(self, event):
        logging.debug('right_click')
        
    def doFirst():
        pass
        
    def menu(self):
        logging.debug('menu')
        menu = gtk.Menu() 
        
        menuItems = [ 
            ["Start", self.doFirst], 
            ["Reset timer", self.doFirst], 
            [],
            ["Projects", self.doFirst], 
            ["Post time to Basecamp", self.doFirst], 
            [],
            ["Round time", self.doFirst], 
            ["Edit timer", self.doFirst], 
            [],
            ["Show timer", self.doFirst],
        ]
        
        for menuItem in menuItems: 
            if (len(menuItem) > 0):
                item = gtk.MenuItem(menuItem[0], True)
                item.show() 
                item.connect( "activate", *menuItem[1:]) 
            else:
                item = gtk.SeparatorMenuItem()
            menu.add(item)
        
        menu.connect("destroy", self.on_menu_destroy)
        return menu
        
    def on_menu_destroy(self, menu):
        #logging.debug('print self.button.state: %i' % self.button.state)
        #logging.debug('self.button.get_relief(): %s' % self.button.get_relief())
        #self.button.set_relief(gtk.RELIEF_NONE)
        pass

    def setup_rightclick_menu(self):
        xml="""<popup name="button3">
<menuitem name="ItemPreferences" 
          verb="Preferences" 
          label="_Preferences" 
          pixtype="stock" 
          pixname="gtk-preferences"/>
<menuitem name="ItemAbout" 
          verb="About" 
          label="_About" 
          pixtype="stock" 
          pixname="gtk-about"/>
</popup>"""

        verbs = [('About', self.show_about), ('Preferences', self.show_preferences)]
        
        self.applet.setup_menu(xml, verbs, None)

    def show_about(obj, label, *data):
        logging.debug('show_about')
        
    def show_preferences(*arguments):
        logging.debug('show_preferences')

    # when the applet window changes size
    def change_size(self, applet, new_size, image):
        logging.debug('change_size')

        self.do_image(self.image_file, image)

    # when the theme background changes
    def change_background(self, applet, background_type, color, pixmap):
        logging.debug('change_background')

        applet.set_style(None)
        rc_style = gtk.RcStyle()
        applet.modify_style(rc_style)
        
        if background_type == gnomeapplet.NO_BACKGROUND:
            pass
        elif background_type == gnomeapplet.COLOR_BACKGROUND:
            applet.modify_bg(gtk.STATE_NORMAL, color)
        elif background_type == gnomeapplet.PIXMAP_BACKGROUND:
            style = applet.style.copy()
            style.bg_pixmap[gtk.STATE_NORMAL] = pixmap
            applet.set_style(style)

    # when the applet is clicked
    def button_press(self, button, event):
        logging.debug('button_press')

        # left mouse button
        if event.button == 1:
            self.left_click(event)
            
        # scroll wheel mouse button
        elif event.button == 2:
            pass

        # right mouse button
        elif event.button == 3:
            self.right_click(event)
            button.emit_stop_by_name("button_press_event") #else the menu doesn't show

#@todo: fix this
class PanelButton(gtk.MenuBar):
    def __init__(self):
        pass

# function to run/register the class
def BaseCampTimer_factory(applet, iid):
    applet.set_applet_flags(gnomeapplet.EXPAND_MINOR)
    BaseCampTimer_Applet(applet, iid)
    
    applet.show_all()
    applet.set_background_widget(applet)
    return True

if __name__ == '__main__':
    gobject.type_register(gnomeapplet.Applet)

    # Use parameter "run-in-window" to just run as a regular
    # application for debugging purposes
    if len(sys.argv) > 1 and sys.argv[1] == 'run-in-window':
        logging.debug('Running in windowed mode')
        
        # create the main window
        gtk.window_set_default_icon_name(BaseCampTimer_Applet.icon_name)
        main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        main_window.set_title(BaseCampTimer_Applet.title)
        main_window.connect('destroy', gtk.main_quit)
        main_window.set_default_size(24, 24)

        # create the applet and run in the window
        app = gnomeapplet.Applet()
        BaseCampTimer_factory(app, None)
        app.reparent(main_window)

        # run it
        main_window.show_all()
        gtk.main()
    else:
        logging.debug('Running as applet')
        # create as an applet
        gnomeapplet.bonobo_factory('OAFIID:BCTimer_Applet_Factory',
                                   gnomeapplet.Applet.__gtype__,
                                   BaseCampTimer_Applet.title, BaseCampTimer_Applet.version,
                                   BaseCampTimer_factory)
