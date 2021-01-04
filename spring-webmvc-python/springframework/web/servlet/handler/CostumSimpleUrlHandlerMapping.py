import logging
from springframework.web.servlet.handler.SimpleUrlHandlerMapping import SimpleUrlHandlerMapping
from springframework.web.testfixture.servlet import MockHttpServletRequest
from springframework.web.testfixture.servlet import MockHttpServletResponse


class CustomSimpleUrlHandlerMapping(SimpleUrlHandlerMapping):
    
    def __init__(self, urlMap: dict(), mockLookupPath: str):
        super().__init__(urlMap)

    # Simply use path info as target path without decoding
    def init_lookup_path(self, request: MockHttpServletRequest):
        logging.info(f"[request.pathInfo] = {request.pathInfo()}")
        return request.pathInfo()
