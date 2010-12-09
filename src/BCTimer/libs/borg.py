# here is the new-style Borg (not much more complex then the "old-style")
class Borg(object):
    _state = {}
    def __new__(cls, *p, **k):
        print '!!!!!!!!!!!!!!!!!!!!!!!!!!!!!11'
        self = object.__new__(cls, *p, **k)
        
        print cls._state
        
        self.__dict__ = cls._state
        return self
