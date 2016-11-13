def Private(*args):
    
    def decor(cls):
        
        class decorated:
            def __init__(self, *args, **kwargs):
                object.__setattr__(self, "obj", cls(*args, **kwargs))
            
            def __getattr__(self, attr):
                if(args.__contains__(attr)):
                    raise TypeError("Pobranie atrybutu prywatnego: "+attr)
                
                return object.__getattribute__(self.obj, attr)
            
            def __setattr__(self, attr, val):
                if(args.__contains__(attr)):
                    raise TypeError("Pobranie atrybutu prywatnego: "+attr)
                
                return object.__setattr__(self.obj, attr, val)
        
        return decorated
        
    return decor

    
#    def __init__(self, *args):
#        self.l = args
#
#    def __call__(self, cls):
#
#        class dummy:
#
#            def __init__(inst, *args, **kwargs):
#                inst.l = args
#                inst.k = kwargs
#
#            def __getattr__(inst, attr):
#                return inst.l.get(attr)
#
#            def __setattr__(inst, attr, val):
#                pass
#
#            def __call__(inst, *args, **kwargs):
#                return cls(args, kwargs)
#
#        return dummy()
