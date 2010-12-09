from BCTimer.libs import Singleton

class SingletonWindow(Singleton):
    ignoreSubsequent = True
    window = None
    
    def __init__(self):
        self.window.connect('delete-event', self.on_window_delete_event)
    
    def __getattr__(self, name):
        return getattr(self.window, name)
        
    def on_window_delete_event(self, window, event):
        print 'on_window_delete_event'
        window.hide()
        return True
