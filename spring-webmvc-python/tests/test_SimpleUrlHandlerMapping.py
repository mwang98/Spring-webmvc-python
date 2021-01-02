import logging
from springframework.web.servlet.handler import SimpleUrlHandlerMapping
from springframework.web.servlet import HandlerExecutionChain, HandlerMapping
from springframework.utils.mock.inst import HttpServletRequest, HttpServletResponse


class MockController():

    def __init__(self, name: str):
        self.name = name

    def get_name(self) -> str:
        return self.name


class MockSimpleUrlHandlerMapping(SimpleUrlHandlerMapping):

    def __init__(self, urlMap: dict(), mockLookupPath: str):
        super().__init__(urlMap)
        self.mockLookupPath = mockLookupPath

    def init_lookup_path(self, request):
        return self.mockLookupPath


def test_init_lookup_path(urlMap: dict(), request: HttpServletRequest):
    handlerMapping: HandlerMapping = SimpleUrlHandlerMapping(urlMap)
    print(handlerMapping.init_lookup_path(request))

def test_register_handlers(urlMap: dict()):
    handlerMapping: HandlerMapping = SimpleUrlHandlerMapping(urlMap)
    handlerMapping.init_application_context()

def test_mapping_directly(urlMap: dict, request: HttpServletRequest, lookupPath: str, response: HttpServletResponse):
    handlerMapping: HandlerMapping = MockSimpleUrlHandlerMapping(urlMap, lookupPath)
    handlerMapping.init_application_context()
    mappedHandler: HandlerExecutionChain = handlerMapping.get_handler(request)
    ha = mappedHandler.get_handler()
    print("mappedHandler: ", mappedHandler)
    print("handlerName: ", ha.name)
    print("preHandle: ", mappedHandler.apply_pre_handle(request, response))
    mappedHandler.apply_post_handle(request, response, None)
    print("postHandle pass")

def test_end_to_end(urlMap: dict(), request: HttpServletRequest):
    handlerMapping: HandlerMapping = SimpleUrlHandlerMapping(urlMap)
    handlerMapping.init_application_context()
    mappedHandler: HandlerExecutionChain = handlerMapping.getHandler(request)

def main():
    urlMap = {"/": MockController("/"), "test": MockController("test")}
    request = HttpServletRequest("GET", "/myservlet/handler.do")
    request.set_context_path("/mycontext")
    request.set_servlet_path("/myservlet")
    request.set_path_info(";mypathinfo")
    request.set_query_string("?param1=value1")
    response = HttpServletResponse()
    test_init_lookup_path(urlMap, request)
    test_register_handlers(urlMap)
    test_mapping_directly(urlMap, request, "/test", response)
    

if __name__ == "__main__":
    main()