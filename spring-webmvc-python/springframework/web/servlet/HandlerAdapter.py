from abc import ABC, abstractmethod

from springframework.web.testfixture.servlet.MockHttpServletRequest import MockHttpServletRequest as HttpServletRequest
from springframework.web.testfixture.servlet.MockHttpServletRequest import MockHttpServletResponse as HttpServletResponse
from springframework.web.servlet import ModelAndView

class HandlerAdapter(ABC):
    @abstractmethod
    def supports(handler) -> bool:
        raise NotImplementedError

    @abstractmethod
    def handle(request: HttpServletRequest, response: HttpServletResponse, handler) -> ModelAndView:
        raise NotImplementedError

    @abstractmethod
    def getLastModified(request: HttpServletRequest, handler) -> long:
        raise NotImplementedError