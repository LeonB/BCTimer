#!/usr/bin/env python

__author__= "Leon Bogaert"
__email__ = "leon@tim-online.nl"
__date__ = "$Nov 27, 2010 11:37:38 AM$"

import pygtk
#pygtk.require('2.0')

import gtk
import gnomeapplet
import gobject
import sys
import logging
from logging.handlers import SysLogHandler

class BaseCampTimer_Applet(gnomeapplet.Applet):
    title = 'Basecamp Timer'
    version = '0.0.1'
    icon_name = 'network-offline'

    logging.basicConfig(level=logging.DEBUG)
    syslog = SysLogHandler(address='/dev/log')
    logger = logging.getLogger()
    logger.addHandler(syslog)

    def __init__(self, applet, iid):
        logging.debug('__init__')

        # save the applet object
        self.applet = applet

        # determine the size to draw the icon
        size = self.applet.get_size() - 2
        
        #Get theme, find SVG icon and put it in a pixbuf
        theme = gtk.icon_theme_get_default()
        pixbuf = theme.load_icon(self.icon_name, size, gtk.ICON_LOOKUP_FORCE_SVG)
        
        #Load image
        image = gtk.image_new_from_pixbuf(pixbuf)

        # set up the applet tooltip
        self.applet.set_tooltip_text(self.title)

        self.button = gtk.Button()
       # self.button.set_label("sad asd asdasd asd asd s ")
        #self.button.set_relief(gtk.RELIEF_HALF)
        #self.button.set_relief(gtk.RELIEF_NORMAL)
        self.button.set_relief(gtk.RELIEF_NONE)
        self.button.set_image(image)

        self.button.connect('button-press-event', self.button_press)
        #self.applet.connect('change-size', self.change_size, image)
        #self.applet.connect('change-background', self.change_background)
        
        self.applet.add(self.button)
        self.applet.show_all()

    def left_click(self, event):
        logging.debug('left_click')
        #self.show_leftclick_menu(event)
        self.menu().popup(None, None, self.menu_position, event.button, event.time)
        return gtk.TRUE
        
    def menu_position(self, menu):
        label = self.button.get_allocation()
        window = menu.get_allocation()
        screen = self.button.get_screen()

        x, y = self.button.get_parent_window().get_origin()
        menu_w, menu_h = menu.size_request()
        
        logging.debug("y: %i" % y)
        logging.debug("label.height: %i" % label.height)
        logging.debug("self.button.get_screen().get_height(): %i" % self.button.get_screen().get_height())
        logging.debug("window.height: %i" % window.height)
        logging.debug("menu_w: %i" % menu_w)
        logging.debug("menu_h: %i" % menu_h)

        self.popup_dir = self.applet.get_orient()

        if self.popup_dir in (gnomeapplet.ORIENT_DOWN, gnomeapplet.ORIENT_UP):
            if self.popup_dir == gnomeapplet.ORIENT_DOWN:
                #y = y + label.height
                y = self.applet.get_size()
            else:
                y = screen.get_height() - self.applet.get_size() - menu_h

            screen_w = self.button.get_screen().get_width()
            if x + window.width > screen_w:
                x = screen_w - window.width

        elif self.popup_dir in (gnomeapplet.ORIENT_RIGHT, gnomeapplet.ORIENT_LEFT):
            if self.popup_dir == gnomeapplet.ORIENT_RIGHT:
                x = x + label.width
            else:
                x = x - window.width

            screen_h = self.button.get_screen().get_height()
            if y + window.height > screen_h:
                y = screen_h - window.height
              
        logging.debug(x)
        logging.debug(y)

        return (x, y, 0)
        
    def right_click(self, event):
        logging.debug('right_click')
        
    def doFirst():
        pass
        
    def doSecond():
        pass
        
    def doThird():
        pass
        
    def menu(self):
        logging.debug('menu')
        menu = gtk.Menu() 
        
        menuItems = [ 
            ["first", self.doFirst], 
            ["second", self.doSecond], 
            ["third", self.doThird]] 
        
        for menuItem in menuItems: 
            item = gtk.MenuItem(menuItem[0], True) 
            item.show() 
            item.connect( "activate", *menuItem[1:]) 
            menu.add(item)
        
        return menu

    def setup_rightclick_menu(self):
        xml="""<popup name="button3">
<menuitem name="ItemPreferences" 
          verb="Preferences" 
          label="_Preferences" 
          pixtype="stock" 
          pixname="gtk-preferences"/>
<separator/>
<submenu name="Submenu" _label="Su_bmenu">
<menuitem name="ItemAbout" 
          verb="About" 
          label="_About" 
          pixtype="stock" 
          pixname="gtk-about"/>
</submenu>
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
            button.emit_stop_by_name("button_press_event")
            
class PanelButton(gtk.ToggleButton):
    def __init__(self):
        gtk.ToggleButton.__init__(self)
        self.set_relief(gtk.RELIEF_NONE)
        self.set_border_width(0)

        self.label = gtk.Label()
        self.label.set_justify(gtk.JUSTIFY_CENTER)

        self.label.connect('style-set', self.on_label_style_set)
        self.connect('size_allocate', self.on_size_allocate)
        self.connect('button_press_event', self.on_button_press)

        self.add(self.label)

        self.activity, self.duration = None, None
        self.prev_size = 0


        # remove padding, so we fit on small panels (adapted from clock applet)
        gtk.rc_parse_string ("""style "hamster-applet-button-style" {
                GtkWidget::focus-line-width=0
                GtkWidget::focus-padding=0
            }

            widget "*.hamster-applet-button" style "hamster-applet-button-style"
        """);
        gtk.Widget.set_name (self, "hamster-applet-button");


    def set_active(self, is_active):
        self.set_property('active', is_active)

    def set_text(self, activity, duration):
        activity = stuff.escape_pango(activity)
        if len(activity) > 25:  #ellipsize at some random length
            activity = "%s%s" % (activity[:25], "&#8230;")

        self.activity = activity
        self.duration = duration
        self.reformat_label()

    def reformat_label(self):
        label = self.activity
        if self.duration:
            if self.use_two_line_format():
                label = "%s\n%s" % (self.activity, self.duration)
            else:
                label = "%s %s" % (self.activity, self.duration)

        label = '<span gravity="south">%s</span>' % label
        self.label.set_markup("") #clear - seems to fix the warning
        self.label.set_markup(label)

    def use_two_line_format(self):
        if not self.get_parent():
            return False

        popup_dir = self.get_parent().get_orient()

        orient_vertical = popup_dir in [gnomeapplet.ORIENT_LEFT] or \
                          popup_dir in [gnomeapplet.ORIENT_RIGHT]


        context = self.label.get_pango_context()
        metrics = context.get_metrics(self.label.style.font_desc,
                                      pango.Context.get_language(context))
        ascent = pango.FontMetrics.get_ascent(metrics)
        descent = pango.FontMetrics.get_descent(metrics)

        if orient_vertical == False:
            thickness = self.style.ythickness;
        else:
            thickness = self.style.xthickness;

        focus_width = self.style_get_property("focus-line-width")
        focus_pad = self.style_get_property("focus-padding")

        required_size = 2 * ((pango.PIXELS(ascent + descent) ) + 2 * (focus_width + focus_pad + thickness))

        if orient_vertical:
            available_size = self.get_allocation().width
        else:
            available_size = self.get_allocation().height

        return required_size <= available_size

    def on_label_style_set(self, widget, something):
        self.reformat_label()

    def on_size_allocate(self, widget, allocation):
        if not self.get_parent():
            return

        self.popup_dir = self.get_parent().get_orient()

        orient_vertical = True
        new_size = allocation.width
        if self.popup_dir in [gnomeapplet.ORIENT_LEFT]:
            new_angle = 270
        elif self.popup_dir in [gnomeapplet.ORIENT_RIGHT]:
            new_angle = 90
        else:
            new_angle = 0
            orient_vertical = False
            new_size = allocation.height

        if new_angle != self.label.get_angle():
            self.label.set_angle(new_angle)

        if new_size != self.prev_size:
            self.reformat_label()

        self.prev_size = new_size

    def on_button_press(self, widget, event):
        # this allows dragging applet around panel and friends
        if event.button != 1:
            widget.stop_emission('button_press_event')
        return False

# function to run/register the class
def BaseCampTimer_factory(applet, iid):
    BaseCampTimer_Applet(applet, iid)
    return gtk.TRUE

if __name__ == '__main__':
    gobject.type_register(BaseCampTimer_Applet)

    # Use parameter "run-in-window" to just run as a regular
    # application for debugging purposes
    if len(sys.argv) > 1 and sys.argv[1] == 'run-in-window':
        # create the main window
        main_window = gtk.Window(gtk.WINDOW_TOPLEVEL)
        main_window.set_title(BaseCampTimer_Applet.title)
        main_window.connect('destroy', gtk.main_quit)
        main_window.set_default_size(36, 36)

        # create the applet and run in the window
        app = gnomeapplet.Applet()
        BaseCampTimer_factory(app, None)
        app.reparent(main_window)

        # run it
        main_window.show_all()
        gtk.main()
    else:
        # create as an applet
        gnomeapplet.bonobo_factory('OAFIID:BCTimer_Applet_Factory',
                                   BaseCampTimer_Applet.__gtype__,
                                   BaseCampTimer_Applet.title, BaseCampTimer_Applet.version,
                                   BaseCampTimer_factory)
