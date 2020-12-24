from mock.inst import Locale
# TODO: import MediaType, ServerWebExchange

class RedirectView(AbstractUrlBasedView):

    # TODO: _URI_TEMPLATE_VARIABLE_PATTERN
    # TODO: _statusCode
    _contextRelative = True
    _propagateQuey = False
    
    __init__(self, redirectUrl: str = None, statusCode: HttpStatus = None):
        super(redirectUrl)
        setStatusCode(statusCode)

    def setStatusCode(statusCode: HttpStatus) -> None:
        assert statusCode.is3xxRedirection()
        self.statusCode = statusCode

    def getStatusCode() -> HttpStatus:
        return self.statusCode

    def setContextRelative(contextRelative: bool) -> None:
        self.contextRelative = contextRelative

    def isContextRelative() -> bool:
        return self.contextRelative

    def isPropogateQuery() -> bool:
        return self.propagateQuery

    def setHosts(hosts: list) -> None:
        self.hosts = hosts
    
    def getHosts() -> list:
        return self.hosts

    def afterPropertiesSet() -> None:
        super.afterPropertiesSet()

    def isRedirectView() -> bool:
        return True

    def checkResourceExists(locale: Locale) -> bool:
        return True

    def renderInternal(model: dict, contenType: object, exchange: ServerWebExchange) -> dict:
        return sendRedirect(targetUrl, exchange)

    def createTargetUrl(model: dict, exchange: ServerWebExchange) -> str:
        url = getUrl()
        assert url is not None, "'url' not set"

        request = exchange.getRequest()

        # targetUrl = StringBuilder()
        # if (isContextRelative() and url.startsWith("/")):
        #     targetUrl.append()


    def getCurrentUriVariables(exchange: ServerWebExchange) -> dict:
        name = HandlerMapping.URI_TEMPLATE_VARIABLES_ATTRIBUTE
        return exchange.getAttributeOrDefault(name, Collections.emptyMap())

    # def expandTargetUrlTemplate()

    def encodeUriVariable(text: str) -> str:
        return UriUtils.encode(text, StandardCharsts.UTF_8)

    # def appendCurrentRequestQuery()

    # def sendRedirect()

    def isRemoteHost(targetUrl: str) -> bool:
        if (ObjectUtils.isEmpty(self.hosts)):
            return False
        
        targetHost = UriCoponentsBuilder.fromUriString(targetUrl).build().getHost()
        if not StringUtils.hasLength(targetHost):
            return False

        for host in self.hosts:
            if targetHost == host:
                return False

        return True


    

    

