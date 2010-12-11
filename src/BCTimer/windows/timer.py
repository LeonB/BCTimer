import gtk
import pango
import BCTimer
from BCTimer.windows.singletonwindow import SingletonWindow

class Timer(SingletonWindow):
    def __init__(self, app):
        self.app = app
        self.new_stopwatch()
        
        builder = gtk.Builder()
        builder.add_from_file(BCTimer.App.ROOTDIR + '/' + 'timer.glade') 
        
        self.window = builder.get_object("windowTimer")
        self.entry_time = builder.get_object("entryTime")
        self.image_play = builder.get_object("imagePlay")
        
        builder.connect_signals(self)
        
        super(self.__class__, self).__init__()
        
    def new_stopwatch(self):
        self.stopwatch = BCTimer.models.Stopwatch()
        self.stopwatch.connect('start-event', self.on_Stopwatch_startEvent)
        self.stopwatch.connect('stop-event', self.on_Stopwatch_stopEvent)
        self.stopwatch.connect('minute-signal', self.on_Stopwatch_minuteSignal)
        self.stopwatch.connect('second-signal', self.on_Stopwatch_secondSignal)
        
    def expose(self, widget, event):
        pass
        
    def on_buttonPlay_clicked(self, widget):
        if self.stopwatch.is_running:
            self.stopwatch.stop()
            self.stopwatch.save()
            
            #Nieuwe stopwatch aanmaken
            self.new_stopwatch()
        else:
            self.stopwatch.start()
            
    def on_Stopwatch_startEvent(self, stopwatch):
        icon, size = self.image_play.get_stock()
        self.image_play.set_from_stock(gtk.STOCK_MEDIA_STOP,  size)
        
    def on_Stopwatch_stopEvent(self, stopwatch):
        icon, size = self.image_play.get_stock()
        self.image_play.set_from_stock(gtk.STOCK_MEDIA_PLAY,  size)

    def on_Stopwatch_secondSignal(self, stopwatch):
        print 'second'
        
    def on_Stopwatch_minuteSignal(self, stopwatch):
        print 'minute'
