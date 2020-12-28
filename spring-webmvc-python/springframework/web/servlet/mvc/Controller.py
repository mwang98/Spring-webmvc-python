from abc import ABC, abstractmethod

from springframework.web.testfixture.servlet.MockHttpServletRequest import MockHttpServletRequest as HttpServletRequest
from springframework.web.testfixture.servlet.MockHttpServletRequest import MockHttpServletResponse as HttpServletResponse
from springframework.web.servlet import ModelAndView

class Controller(ABC){
    @abstractmethod
    def handleRequest(request: HttpServletRequest, response: HttpServletResponse) -> ModelAndView:
        raise NotImplementedError
}