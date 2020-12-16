from abc import ABC, abstractmethod


class View(ABC):
    
    def __init__(self):
        self.RESPONSE_STATUS_ATTRIBUTE = self.__class__.__name__ + ".responseStatus"
        self.PATH_VARIABLES = self.__class__.__name__ + ".pathVariables"
        self.SELECTED_CONTENT_TYPE = self.__class__.__name__ + ".selectedContentType"

    def get_content_type(self):
        return None

    @abstractmethod
    def render(self, request, response, model=None):
        raise NotImplementedError
