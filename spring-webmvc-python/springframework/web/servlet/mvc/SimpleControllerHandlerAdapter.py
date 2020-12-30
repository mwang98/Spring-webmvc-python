from springframework.web.servlet import ModelAndView
from springframework.web.servlet.HandlerAdapter import HandlerAdapter
from springframework.web.servlet.mvc.Controller import Controller
from springframework.utils.mock.inst import HttpServletResponse, HttpServletRequest


class SimpleControllerHandlerAdapter(HandlerAdapter):
    def supports(self, handler: object) -> bool:
        return isinstance(handler, Controller)

    def handle(self, request: HttpServletRequest, response: HttpServletResponse, handler: object) -> ModelAndView:
        handler: Controller = handler
        return handler.handleRequest(request, response)

    def get_last_modified(self, request: HttpServletRequest, handler: object) -> int:
        if isinstance(handler, Controller):
            handler: Controller = handler
            return handler.getLastModified(request)
        return -1
 