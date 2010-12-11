import gobject
gobject.threads_init()
import threading

class Stopwatch(gobject.GObject):
    #name, ?, #return type, #arguments
    __gsignals__ = {
        "second-signal": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()), #Mhzzz....
        "minute-signal": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
        "save-event": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
        "start-event": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
        "stop-event": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
        "pause-event": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, ()),
    }

    def __init__(self):
        super(self.__class__, self).__init__()
        self.is_running = False
        self.seconds = 0
        self.minutes = 0
        
        self.connect('start-event', self.start_timer)
        self.connect('stop-event', self.stop_timer)
        
    def start(self):
        self.emit('start-event')
        
    def pause(self):
        pass
        
    def stop(self):
        self.emit('stop-event')
        pass
        
    def toggle(self):
        if (self.is_running):
            self.stop()
        else:
            self.start()
        
    def load(self, id):
        pass
        
    def save(self):
        pass
        
    def sync(self):
        '''OK, wat te doen? Moet ik deze aanmaken of op basis van een callback???'''
        pass
        
    '''Callbacks'''
    def start_timer(self, stopwatch):
        self.is_running = True
        print 'Starting timerzz....'
        #http://faq.pygtk.org/index.py?file=faq20.006.htp&req=show
        #self.second_timer = threading.Timer(1.0, self.aaah)
        #self.minute_timer = threading.Timer(60.0, lambda self: self.emit('minute-signal'))

        #self.second_timer = threading.Timer(1.0, self.emit_second_signal)
        #self.minute_timer = threading.Timer(60.0, self.emit_minute_signal)
        self.second_timer = RepeatTimer(1.0, self.emit_second_signal).start()
        self.minute_timer = RepeatTimer(60.0, self.emit_minute_signal).start()
        self.second_timer.start()
        self.minute_timer.start()
        return True

        gobject.timeout_add(1 * 1000, self.emit_second_signal)
        gobject.timeout_add(60 * 1000, self.emit_minute_signal)
        
        #self.second_timer.start()
        #self.minute_timer.start()
        
    def emit_second_signal(self):
        if (self.is_running == False):
            return False
            
        self.emit('second-signal')
        self.seconds = self.seconds + 1
        import time
        print self.seconds
        return True
        
    def emit_minute_signal(self):
        if (self.is_running == False):
            return False
        
        self.emit('minute-signal')
        self.minutes = self.minutes + 1
        print self.minutes
        return True
        
    def stop_timer(self, stopwatch):
        print 'Stopping timerzz....'
        self.is_running = False
        
gobject.type_register(Stopwatch)
        
#~ if __name__ == '__main__':
    #~ def before_start(stopwatch):
        #~ print stopwatch
        #~ 
    #~ def start(stopwatch):
        #~ print 'start'
        #~ print stopwatch.is_running
        #~ 
    #~ def after_start(stopwatch):
        #~ print 'after_start'
        #~ print stopwatch.is_running
    #~ 
    #~ stopwatch = Stopwatch()
    #~ 
    #~ stopwatch.connect('start-event', start)
    #~ #timer.connect_before('start-event', before_start)
    #~ stopwatch.connect_after('start-event', after_start)
    #~ 
    #~ print stopwatch.is_running
    #~ print 'Going to start'
    #~ stopwatch.start()

# Copyright (c) 2009 Geoffrey Foster
# 
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation
# files (the "Software"), to deal in the Software without
# restriction, including without limitation the rights to use,
# copy, modify, merge, publish, distribute, sublicense, and/or sell
# copies of the Software, and to permit persons to whom the
# Software is furnished to do so, subject to the following
# conditions:
# 
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
# 
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES
# OF MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT
# HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY,
# WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR
# OTHER DEALINGS IN THE SOFTWARE.
 
from threading import Event, Thread, Timer
import time as Time
 
class RepeatTimer(Thread):
    def __init__(self, interval, function, iterations=0, args=[], kwargs={}):
        Thread.__init__(self)
        self.interval = interval
        self.function = function
        self.iterations = iterations
        self.args = args
        self.kwargs = kwargs
        self.finished = Event()
 
    def run(self):
        count = 0
        time = Time.time()
        while not self.finished.is_set() and (self.iterations <= 0 or count < self.iterations):
            interval_correction = round((Time.time() - time), 3) % self.interval
            print interval_correction
            self.finished.wait(self.interval - interval_correction)
            if not self.finished.is_set():
                threading.Thread(None, self.function, *self.args, **self.kwargs).start()
                #threading.Timer(self.interval - interval_correction, self.function, *self.args, **self.kwargs).start()
                count += 1
 
    def cancel(self):
        self.finished.set()
