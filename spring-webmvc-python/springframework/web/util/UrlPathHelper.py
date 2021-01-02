import logging
from springframework.utils.mock.inst import HttpServletRequest
from springframework.web.util.WebUtils import WebUtils


class UrlPathHelperMeta(type):
    
    def __init__(cls, *args, **kwargs):
        cls.PATH_ATTRIBUTE: str = cls.__name__ + ".path"


class UrlPathHelper(metaclass=UrlPathHelperMeta):

    def __init__(self):
        return

    def resolve_and_cache_lookup_path(self, request: HttpServletRequest) -> str:
        lookupPath: str = self.get_lookup_path_for_request(request)
        request.set_attribute(self.PATH_ATTRIBUTE, lookupPath)

    def get_lookup_path_for_request(self, request: HttpServletRequest) -> str:
        pathWithinApp: str = self.get_path_within_application(request)
        # Always use full path within current servlet context {UrlPathHelprt.java: 249}
        return pathWithinApp
        
    def get_path_within_application(self, request: HttpServletRequest) -> str:
        contextPath: str = self.get_context_path(request)
        requestUri: str = self.get_request_uri(request)
        path: str = self.get_remaining_path(requestUri, contextPath, True)
        logging.info(f"\n contextPath: {contextPath} \n requestUri: {requestUri} \n path: {path}")
        if path:
            # Normal case: URI contains context path.
            if path.replace(" ", "") == "":
                return "/"
            else:
                return path
        else:
            return requestUri
    
    def get_context_path(self, request: HttpServletRequest) -> str:
        contextPath: str = str(request.get_attribute(WebUtils.INCLUDE_SERVLET_PATH_ATTRIBUTE))
        if not contextPath:
            contextPath = request.get_context_path()
        if contextPath == "/":
            contextPath = ""
        return self.decode_request_string(request, contextPath)
    
    def get_request_uri(self, request: HttpServletRequest) -> str:
        uri: str = str(request.get_attribute(WebUtils.INCLUDE_REQUEST_URI_ATTRIBUTE))
        if not uri:
            uri = uri.get_request_uri()
        return self.decode_and_clean_uri_string(request, uri)
    
    def decode_request_string(self, request: HttpServletRequest, source: str) -> str:
        # Ignore decode
        return source

    def decode_and_clean_uri_string(self, request: HttpServletRequest, uri: str) -> str:
        uri = self.remove_semicolon_content(uri)
        uri = self.decode_request_string(request, uri)
        uri = self.get_sanitized_path(uri)
        return uri
    
    def remove_semicolon_content(self, requestUri: str) -> str:
        res: str = ""
        state = False
        for i in requestUri:
            if i == ";":
                state = True
            if state == False:
                res = res + i
            if i == "/":
                state = False
        return res
    
    def get_sanitized_path(self, path: str) -> str:
        return path.replace("//", "/")
    
    def get_remaining_path(self, requestUri: str, mapping: str, ignoreCase: bool) -> str:
        index1: int = 0
        index2: int = 0
        while index1 < len(requestUri) and index2 < len(mapping):
            c1: str = requestUri[index1]
            c2: str = mapping[index2]
            if c1 == ",":
                index = requestUri.index('/', index1)
                if index == -1:
                    return None
                c1 = requestUri[index1]
            if c1 == c2 or (ignoreCase and c1.lower() == c2.lower()):
                index1 += 1
                index2 += 1
                continue
            return None

        if index2 != len(mapping):
            return None
        elif index1 == len(requestUri):
            return ""
        elif requestUri[index] == ";":
            index = requestUri.index("/", index1)
        return (requestUri.substring(index1) if index1 != -1 else "")