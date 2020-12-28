from springframework.web.servlet import ModelAndView
from springframework.web.servlet import HandlerAdapter
from springframework.web.servlet.mvc import Controller

class SimpleControllerHandlerAdapter(HandlerAdapter){
    def supports(handler) -> bool:
        return isinstance(handler, Controller)

    def handle(request: HttpServletRequest, response: HttpServletResponse, handler) -> ModelAndView:
        return handler.handleRequest(request, response)

    def getLastModified(request: HttpServletRequest, handler) -> long:
        if isinstance(handler, Controller):
            return handler.getLastModified(request)
        return -1
}