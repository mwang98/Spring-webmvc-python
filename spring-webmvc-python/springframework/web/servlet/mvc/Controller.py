from abc import ABC, abstractmethod

# check for posiible recursive import
from springframework.utils.mock.inst import HttpServletResponse, HttpServletRequest
from springframework.web.servlet import ModelAndView


class Controller(ABC):
    @abstractmethod
    def handleRequest(request: HttpServletRequest, response: HttpServletResponse) -> ModelAndView:
        raise NotImplementedError
