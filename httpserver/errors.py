class InterfaceError:
    def __init__(self,error: str = None):
        self.error = error
        
    def __str__(self):
        return self.error
    
    def __bool__(self):
        if self.error is None:
            return True
        return False