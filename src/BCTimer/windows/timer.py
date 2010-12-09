import gtk
import pango
import BCTimer
from BCTimer.windows.singletonwindow import SingletonWindow

class Timer(SingletonWindow):
    def __init__(self, app):
        self.app = app
        builder = gtk.Builder()
        builder.add_from_file(BCTimer.App.ROOTDIR + '/' + 'timer.glade') 
        self.window = builder.get_object("windowTimer")
        self.entry_time = builder.get_object("entryTime")
        
        builder.connect_signals(self)
        builder.get_object("windowTimer").connect_after('expose-event', self.expose)
        
        super(self.__class__, self).__init__()
        
    def expose(self, widget, event):
        #~ w = self.window
        #~ 
        #~ width, height = widget.window.get_size()
        #~ 
        #~ print width, height
        #~ 
        width = 400
        height = 174
        #~ 
        #~ self.window.window.draw_line(w.style.black_gc, 0, 0, width, height)
        #~ self.window.window.draw_line(w.style.black_gc, 0, height, width, 0)
        
        self.context = widget.window.cairo_create()
        self.context.move_to(0, 0)
        self.context.line_to(width, height)
        
        self.context.move_to(width,0)
        self.context.line_to(0, height)
        
        self.context.stroke()
        
    #~ def on_entryTime_focus_in_event(self, event, widget):
        #~ print 'on_entryTime_focus'
        #~ self.entry_time.set_has_frame(True)
        #~ 
    #~ def on_entryTime_focus_out_event(self, event, widget):
        #~ print 'on_entryTime_focus'
        #~ self.entry_time.set_has_frame(False)
        #~ 
    #~ def on_entryTime_realize(self, event):
        #~ self.entry_time.set_text('Enter new font size here')
        #~ font_description = pango.FontDescription('Lucida Sans %s' % 24)
        #~ self.entry_time.modify_font(font_description)
        #~ 
        #~ self.entry_time.modify_base(gtk.STATE_NORMAL, self.window.style.bg[gtk.STATE_NORMAL])
        #~ print self.window.style.bg[gtk.STATE_NORMAL]
        #~ self.entry_time.set_has_frame(False)
        #~ print self.entry_time.get_focus_padding()
