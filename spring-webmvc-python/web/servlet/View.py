class View():
    
    def __init__(self):
        
        self.RESPONSE_STATUS_ATTRIBUTE = self.__class__.__name__ + ".responseStatus"
        self.PATH_VARIABLES = self.__class__.__name__ + ".pathVariables"
        self.SELECTED_CONTENT_TYPE = self.__class__.__name__ + ".selectedContentType"
        
    def getContentType(self):
        return None
    
    def render(self, request, response, model=None):
        raise NotImplementedError