class Timer(gobject.GObject):
    #name, ?, #return type, #arguments
    __gsignals__ = {
      "some-signal": (gobject.SIGNAL_RUN_FIRST, gobject.TYPE_NONE, (object, )),
    }
