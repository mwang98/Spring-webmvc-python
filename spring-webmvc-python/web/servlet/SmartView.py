from web.servlet import View

class SmartView(View):
    
    def __init__(self):
        raise NotImplementedError
        
    def isRedirectView(self):
        raise NotImplementedError