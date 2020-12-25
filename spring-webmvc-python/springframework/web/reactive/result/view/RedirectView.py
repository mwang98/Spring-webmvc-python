from mock.inst import Locale
# TODO: import MediaType, ServerWebExchange

class RedirectView(AbstractUrlBasedView):

    # TODO: _URI_TEMPLATE_VARIABLE_PATTERN
    # TODO: _statusCode
    _contextRelative = True
    _propagateQuey = False
    
    def __init__(self, redirectUrl: str = None, statusCode: HttpStatus = None):
        super().__init__(redirectUrl)
        self.setStatusCode(statusCode)

    def setStatusCode(self, statusCode: HttpStatus) -> None:
        assert statusCode.is3xxRedirection(), "Not a redirect status code"
        self.statusCode = statusCode

    def getStatusCode(self) -> HttpStatus:
        return self.statusCode

    def setContextRelative(self, contextRelative: bool) -> None:
        self.contextRelative = contextRelative

    def isContextRelative(self) -> bool:
        return self.contextRelative

    def isPropogateQuery(self) -> bool:
        return self.propagateQuery

    def setHosts(self, hosts: list) -> None:
        self.hosts = hosts
    
    def getHosts(self) -> list:
        return self.hosts

    def afterPropertiesSet(self) -> None:
        super().afterPropertiesSet()

    def isRedirectView(self) -> bool:
        return True

    def checkResourceExists(self, locale: Locale) -> bool:
        return True

    def renderInternal(self, model: dict, contenType: object, exchange: ServerWebExchange) -> dict:
        return self.sendRedirect(targetUrl, exchange)

    def createTargetUrl(self, model: dict, exchange: ServerWebExchange) -> str:
        url = self.getUrl()
        assert url is not None, "'url' not set"

        request = exchange.getRequest()

        # targetUrl = StringBuilder()
        # if (isContextRelative() and url.startsWith("/")):
        #     targetUrl.append()


    def getCurrentUriVariables(self, exchange: ServerWebExchange) -> dict:
        # TODO: HandlerMapping
        pass
        # name = HandlerMapping.URI_TEMPLATE_VARIABLES_ATTRIBUTE
        # return exchange.getattr(name, Collections.emptyMap())

    # def expandTargetUrlTemplate()

    def encodeUriVariable(self, text: str) -> str:
        # TODO: UriUtils
        pass
        # return UriUtils.encode(text, StandardCharsts.UTF_8)

    # def appendCurrentRequestQuery()

    # def sendRedirect()

    def isRemoteHost(self, targetUrl: str) -> bool:
        if self.hosts is not None:
            return False
        # TODO: UricomponentsBuilder
        # targetHost = UriComponentsBuilder.fromUriString(targetUrl).build().getHost()
        # if not StringUtils.hasLength(targetHost):
        #     return False

        for host in self.hosts:
            if targetHost == host:
                return False

        return True


    

    

