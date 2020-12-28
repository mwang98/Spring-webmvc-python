import re
from springframework.web.servlet import SmartView
from springframework.web.servlet.view import AbstractUrlBasedView
from springframework.utils.mock.inst import HttpStatus


class RedirectView(SmartView, AbstractUrlBasedView):

    URI_TEMPLATE_VARIABLE_PATTERN = re.compile("\\{([^/]+?)\\}")
    contextRelative: bool = False
    http10Compatible: bool = True
    exposeModelAttributes: bool = True
    encodingScheme: str = None
    statusCode: HttpStatus = None
    expandUriTemplateVariables: bool = True
    propagateQueryParams: bool = False
    hosts = list()

    def __init__(
        self,
        url: str,
        contextRelative: bool = None,
        http10Compatible: bool = None,
            exposeModelAttributes: bool = None):

        super().__init__(url)
        self.contextRelative = contextRelative
        self.http10Compatible = http10Compatible
        self.exposeModelAttributes = exposeModelAttributes
        self.setExposePathVariables(False)

    def setContextRelative(self, contextRelative: bool) -> None:
        self.contextRelative = contextRelative

    def setHttp10Compatible(self, http10Compatible: bool) -> None:
        self.http10Compatible = http10Compatible

    def setExposeModelAttributes(self, exposeModelAttributes: bool) -> None:
        self.exposeModelAttributes = exposeModelAttributes

    def setEncodingScheme(self, encodingScheme: str):
        self.encodingScheme = encodingScheme

    def setStatusCode(self, statusCode: HttpStatus):
        self.statusCode = statusCode

    def setExpandUriTemplateVariables(self, expandUriTemplateVariables: bool) -> None:
        self.expandUriTemplateVariables = expandUriTemplateVariables

    def setPropagateQueryParams(self, propagateQueryParams: bool) -> None:
        self.propagateQueryParams = propagateQueryParams

    def isPropagateQueryProperties(self) -> bool:
        return self.propagateQueryParams

    def setHosts(self, hosts: list) -> None:
        self.hosts = hosts

    def getHosts(self) -> list:
        return self.hosts

    def isRedirectView(self) -> bool:
        return True

    def isContextRequired(self) -> bool:
        return False

    def renderMergedOutputModel(self, model: dict, request, response) -> None:
        targetUrl: str = self.createTargetUrl(model, request)
        targetUrl = self.updateTargetUrl(targetUrl, model, request, response)

        # Save flash attributes
        # RequestContextUtils.saveOutputFlashMap(targetUrl, request, response)

        # Redirect
        self.sendRedirect(request, response, targetUrl, self.http10Compatible)

    def createTargetUrl(self, model: dict, request) -> str:
        # TODO: StringBuilder
        targetUrl = StringBuilder()
        url: str = self.getUrl()
        assert url is not None, "'url' not set"

        if self.contextRelative and self.getUrl().startswith("/"):
            targetUrl.append(self.getContextPath(request))
        targetUrl.append(self.getUrl())

        enc: str = self.encodingScheme
        if enc is None:
            enc = request.getCharacterEncoding()
        if enc is None:
            # TODO: WebUtils
            enc = WebUtils.DEFAULT_CHARACTER_ENCODING

        if self.expandUriTemplateVariables and targetUrl:
            variables: dict = self.getCurrentRequestUriVariables(request)
            targetUrl = self.replaceUriTemplateVariables(str(targetUrl), model, variables, enc)
        if self.isPropagateQueryProperties():
            self.appendCurrentQueryParams(targetUrl, request)
        if self.exposeModelAttributes:
            self.appendQueryProperties(targetUrl, model, enc)

        return str(targetUrl)

    def getContextPath(self, request) -> str:
        contextPath: str = request.getContextPath()
        while contextPath.startsWith("//"):
            contextPath = contextPath[1:]
        return contextPath







