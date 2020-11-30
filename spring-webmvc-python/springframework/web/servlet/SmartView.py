from springframework.web.servlet import View

class SmartView(View):
        
    def isRedirectView(self):
        raise NotImplementedError