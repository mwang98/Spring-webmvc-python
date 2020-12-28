from springframework.web.servlet import ModelAndView
from springframework.web.servlet.HandlerAdapter import HandlerAdapter
from springframework.web.servlet.mvc.Controller import Controller
from springframework.utils.mock.inst import HttpServletResponse, HttpServletRequest


class SimpleControllerHandlerAdapter(HandlerAdapter):
    def supports(self, handler) -> bool:
        return isinstance(handler, Controller)

    def handle(self, request: HttpServletRequest, response: HttpServletResponse, handler) -> ModelAndView:
        return handler.handleRequest(request, response)

    def get_last_modified(self, request: HttpServletRequest, handler) -> int:
        if isinstance(handler, Controller):
            return handler.getLastModified(request)
        return -1
