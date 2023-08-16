class RouterException(Exception):
    def __init__(self,*args):
        super(RouterException,self).__init__(*args)
        
class ResponseException(Exception):
    def __init__(self,*args):
        super(ResponseException,self).__init__(*args)