from unittest import mock
import pytz
from collections import defaultdict
from datetime import datetime

from .MockServletContext import MockServletContext


# inherit HttpServletRequestInterface
class MockHttpServletRequest():

    HTTP = "http"
    HTTPS = "https"
    CHARSET_PREFIX = "charset"
    GMT = pytz.timezone('GMT')
    EMPTY_SERVLET_INPUT_STREAM = mock.MagicMock(name=EMPTY_SERVLET_INPUT_STREAM)
    EMPTY_BUFFERED_READER: mock.MagicMock(name=EMPTY_BUFFERED_READER)
    DATE_FORMATS = [
        "%a %b %d %H:%M:%S %Y",
        "%a, %d-%b-%y %H:%M:%S %Z",
        "%a, %d %b %Y %H:%M:%S %Z"
    ]

    # Public constants
    DEFAULT_PROTOCOL = "HTTP/1.1"
    DEFAULT_SCHEME: str = HTTP
    DEFAULT_SERVER_ADDR = "127.0.0.1"
    DEFAULT_SERVER_NAME = "localhost"
    DEFAULT_SERVER_PORT = 80
    DEFAULT_REMOTE_ADDR = "127.0.0.1"
    DEFAULT_REMOTE_HOST = "localhost"

    # Lifecycle properties
    servletContext = None  # mock
    active = True

    # ServletRequest properties
    attributes = dict()
    characterEncoding: str = None
    content: bytes = None
    contentType: str = None
    inputStream = None  # mock
    reader = None  # mock
    parameters = dict()
    protocol: str = DEFAULT_PROTOCOL
    scheme: str = DEFAULT_SCHEME
    serverName: str = DEFAULT_SERVER_NAME
    serverPort: int = DEFAULT_SERVER_PORT
    remoteAddr: str = DEFAULT_REMOTE_ADDR
    remoteHost: str = DEFAULT_REMOTE_HOST
    locales = list()
    secure = False
    remotePort: int = DEFAULT_SERVER_PORT
    localName: str = DEFAULT_SERVER_NAME
    localAddr: str = DEFAULT_SERVER_ADDR
    localPort: int = DEFAULT_SERVER_PORT
    asyncStarted = False
    asyncSupported = False
    asyncContext = None
    dispatcherType = DispatcherType.REQUEST

    # HttpServletRequest properties
    authType: str = None
    cookies: list = None
    headers = defaultdict(set)
    HeaderValueHolder = set  # use set
    method: str = None
    pathInfo: str = None
    contextPath: str = ""
    queryString: str = None
    remoteUser: str = None
    userRoles = set()
    userPrincipal = None  # mock
    requestedSessionId: str = None
    requestURI: str = None
    servletPath: str = ""
    session = None  # mock
    requestedSessionIdValid = True
    requestedSessionIdFromCookie = True
    requestedSessionIdFromURL = True
    parts = dict()

    # mock class
    # ---------------------------------------------------------------------
    # HttpSession : MockHttpSession
    # Principal
    # HeaderValueHolder : set
    # HttpHeaders
    # DispatcherType : Enum
    # AsyncContext : MockAsyncContext
    # RequestDispatcher : MockRequestDispatcher
    # BufferedReader
    # ServletInputStream
    # Part : MockPart
    # ServletContext : MockServletContext
    # ---------------------------------------------------------------------

    def __init__(self, servletContext=None, method: str = None, requestURI: str = None):
        if servletContext is None:
            self.servletContext = MockServletContext()  # mock
        else:
            self.servletContext = servletContext
        self.method = method
        self.requestURI = requestURI
        self.locales.append("EN")

    # ---------------------------------------------------------------------
    # Lifecycle methods
    # ---------------------------------------------------------------------

    def getServletContext(self):
        return self.servletContext

    def isActive(self) -> bool:
        return self.active

    def close(self) -> None:
        self.active = False

    def invalidate(self) -> None:
        self.close()
        self.clearAttributes()

    def checkActive(self) -> None:
        assert self.active,"Request is not active anymore"

    # ServletRequest interface
    def getAttribute(self, name: str):
        self.checkActive()
        return self.attributes.get(name)

    def getAttributeNames(self) -> list:
        self.checkActive()
        return list(self.attributes.keys())

    def getCharacterEncoding(self) -> str:
        return self.characterEncoding

    def setCharacterEncoding(self, characterEncoding: str) -> None:
        self.characterEncoding = characterEncoding
        self.updateContentTypeHeader()

    def updateContentTypeHeader(self) -> None:
        if self.contentType is not None:
            value = self.contentType
            if (self.characterEncoding is not None) and (self.CHARSET_PREFIX not in this.contentType.lower()):
                value += f";{self.CHARSET_PREFIX}{self.characterEncoding}"
            # TODO: HttpHeaders
            self.doAddHeaderValue(HttpHeaders.CONTENT_TYPE, value, True)

    def setContent(self, context: bytes) -> None:
        self.context = context
        self.inputStream = None
        self.reader = None

    def getContentAsByteArray(self) -> bytes:
        return self.content

    def getContentAsString(self) -> str:
        error_msg = """
        Cannot get content as a String for a null character encoding.
        Consider setting the characterEncoding in the request."
        """
        assert self.characterEncoding is not None, error_msg
        if self.content is None:
            return None
        return self.content.decode + self.characterEncoding

    def getContentLength(self) -> int:
        return -1 if (self.context is None) else len(self.content)

    def getContentLengthLong(self) -> int:
        return self.getContentLength()

    def setContentType(self, contentType: str = None) -> None:
        self.contentType = contentType
        if contentType is not None:
            try:
                # TODO
                mediaType = MediaType.parseMediaType(contentType)
                if mediaType.getCharset() is not None:
                    self.characterEncoding = mediaType.getCharset().name()
            except Exception:
                try:
                    charsetIndex = contentType.lower().index(self.CHARSET_PREFIX)
                    self.characterEncoding = contentType[charsetIndex + len(self.CHARSET_PREFIX):]
                except Exception:
                    pass

            self.updateContentTypeHeader()

    def getContentType(self) -> str:
        return self.contentType

    def getInputStream(self):
        if self.inputStream is not None:
            return self.inputStream
        elif self.reader is not None:
            raise ValueError("Cannot call getInputStream() after getReader() has already been called for the current request")

        if self.content is not None:
            # TODO
            self.inputStream = DelegatingServletInputStream(ByteArrayInputStream(self.content))
        else:
            self.inputStream = self.EMPTY_SERVLET_INPUT_STREAM
        return self.inputStream

    def setParameter(self, name, value) -> None:
        if isinstance(name, dict):
            for key in name:
                assert key is not None, "Parameter map must not be null"
                value = name.get(key)
                if isinstance(value, str) or isinstance(value, list):
                    self.setParameter(key, value)
                else:
                    raise ValueError(f"Parameter map value must be single value or array of type [ String ]")
        elif isinstance(name, str):
            if isinstance(value, str):
                self.parameters[name] = [value]
            elif isinstance(value, list):
                self.parameters[name] = value
            else:
                raise ValueError("!!!")

    def addParameter(self, name, value) -> None:
        if isinstance(name, dict):
            for key in name:
                assert key is not None, "Parameter map must not be null"
                value = name.get(key)
                if isinstance(value, str) or isinstance(value, list):
                    self.addParameter(key, value)
                else:
                    raise ValueError(f"Parameter map value must be single value or array of type [ String ]")
        elif isinstance(name, str):
            if isinstance(value, str):
                self.parameters[name] = [value]
            elif isinstance(value, list):
                old_value = self.parameters.get(name, [])
                self.parameters[name] = old_value + value
            else:
                raise ValueError("!!!")

    def removeParameter(self, name: str) -> None:
        assert name is not None, "Parameter name must not be null"
        self.parameters.pop(name)

    def removeAllParameters(self) -> None:
        self.parameters.clear()

    def getParameter(self, name: str) -> None:
        assert name is not None, "Parameter name must not be null"
        return self.parameters.get(name)

    def getParameterNames(self) -> list:
        return list(self.parameters.keys())

    def getParameterValues(self, name: str) -> list:
        assert name is not None, "Parameter name must not be null"
        return self.parameters.get(name)

    def getParameterMap(self) -> dict:
        return self.parameters

    def setProtocol(self, protocol: str) -> None:
        self.protocol = protocol

    def getProtocol(self) -> str:
        return self.protocol

    def setScheme(self, scheme: str) -> None:
        self.scheme = scheme

    def getScheme(self) -> str:
        return self.scheme

    def setServerName(self, serverName: str) -> None:
        self.serverName = serverName

    def getServerName(self) -> str:
        # TODO: HttpHeaders
        rawHostHeader: str = self.getHeader(HttpHeaders.HOST)
        host = rawHostHeader
        if host is not None:
            host = host.strip()
            if host.startswith('['):
                indexOfClosingBracket = host.index('[')
                if ':' in host:
                    idx = host[indexOfClosingBracket:].index(':')
            if ':' in host::
                idx = host.index(':')
            return host[idx+1:]

        return self.serverPort

    def getReader(self):
        if self.reader is not None:
            return self.reader
        elif self.inputStream is not None:
            raise ValueError("Cannot call getReader() after getInputStream() has already been called for the current request")

        if self.content is not None:
            # TODO
            sourceStream = ByteArrayInputStream(self.content)
            if self.characterEncoding is not None:
                sourceReader = InputStreamReader(sourceStream, self.characterEncoding)
            else:
                sourceReader = InputStreamReader(sourceStream)
            reader = BufferedReader(sourceReader)
        else:
            self.reader = self.EMPTY_BUFFERED_READER
        return self.reader

    def setRemoteAddr(self, remoteAddr: str):
        self.remoteAddr = remoteAddr

    def getRemoteAddr(self) -> str:
        return self.remoteAddr

    def setRemoteHost(self, remoteHost: str) -> None:
        self.remoteHost = remoteHost

    def getRemoteHost(self) -> str:
        return self.remoteHost

    def setAttribute(self, name: str, value=None) -> None:
        self.checkActive()
        assert name is not None, "Attribute name must not be null"
        if value is not None:
            self.attributes[name] = value
        else:
            self.attributes.pop(name)

    def removeAttribute(self, name: str) -> None:
        self.checkActive()
        assert name is not None, "Attribute name must not be null"
        self.attributes.pop(name)

    def clearAttributes(self) -> None:
        self.attributes.clear()

    def addPreferredLocale(self, locales: list) -> None:
        assert locales, "Locale list must not be empty"
        self.locales.clear()
        self.locales.extend(locales)
        self.updateAcceptLanguageHeader()

    def updateAcceptLanguageHeader(self) -> None:
        # TODO: HttpHeaders
        headers = HttpHeaders()
        headers.setAcceptLanguageAsLocales(self.locales)
        self.doAddHeaderValue(HttpHeaders.ACCEPT_LANGUAGE, headers.getFirst(HttpHeaders.ACCEPT_LANGUAGE), True)

    def getLocale(self):
        return self.locales[:1]

    def getLocales(self) -> list:
        return self.locales

    def setSecure(self, secure: bool) -> None:
        self.secure = secure

    def isSecure(self) -> bool:
        return self.secure or self.HTTPS == self.scheme

    def getRequestDispatcher(self, path: str):
        return MockRequestDispatcher(path)

    def getRealPath(self, path: str) -> str:
        return self.servletContext.getRealPath(path)

    def setRemotePort(self, remotePort: int) -> None:
        self.remotePort = remotePort

    def getRemotePort(self) -> str:
        return self.remotePort

    def setLocalName(self, localName: str) -> None:
        self.localName = localName

    def getLocalName(self) -> str:
        return self.localName

    def setLocalAddr(self, localAddr: str) -> None:
        self.localAddr = localAddr

    def getLocalAddr(self) -> str:
        return self.localAddr

    def setLocalPort(self, port: int) -> None:
        self.localPort = localPort

    def getLocalPort(self) -> int:
        return self.localPort

    def startAsync(self, request=None, response=None):
        request = self is request is None
        assert self.asyncSupported, "Async not supported"
        self.asyncStarted = True
        # TODO
        self.asyncContext = MockAsyncContext(request, response)
        return self.asyncContext

    def setAsyncStarted(self, asyncStarted: bool) -> None:
        self.asyncStarted = asyncStarted

    def isAsyncStarted(self) -> bool:
        return self.asyncStarted

    def setAsyncSupported(self, asyncSupported: bool) -> None:
        self.asyncSupported = asyncSupported

    def isAsyncSupported(self) -> bool:
        return self.asyncSupported

    def setAsyncContext(self, asyncContext: MockAsyncContext) -> None:
        self.asyncContext = asyncContext

    def getAsyncContext(self):
        return self.asyncContext

    def setDispatcherType(self, dispatcherType) -> None:
        self.dispatcherType = dispatcherType

    def getDispatcherType(self):
        return self.dispatcherType

    # ---------------------------------------------------------------------
    # HttpServletRequest interface
    # ---------------------------------------------------------------------

    def setAuthType(self, authType: str = None) -> None:
        self.authType = authType

    def getAuthType(self) -> str:
        return self.authType

    def setCookies(self, cookies: list) -> None:
        self.cookies = cookies
        if cookies:
            self.doAddHeaderValue(HttpHeaders.COOKIE, encodeCookies(self.cookies), True)
        else:
            self.removeHeader(HttpHeaders.COOKIE)

    def encodeCookies(self, cookies: list) -> str:
        output = []
        for c in cookies:
            value = "" if c.getValue() is None else c.getValue()
            output.append(f"{c.getName()} = {value}")
        return "; ".join(output)

    def getCookies(self) -> list:
        return self.cookies

    def addHeader(self, name: str, value) -> None:
        # TODO
        pass

    def doAddHeaderValue(self, name: str, value=None, replace: bool) -> None:
        header: HeaderValueHolder = self.headers.get(name)
        assert value is not None, "Header value must not be null"
        if header is None or replace:
            header = HeaderValueHolder()
            self.header[name] = header
        if isinstance(value, set):
            header.update(value)
        elif isinstance(value, list):
            header.update(set(value))
        else:
            header.add(value)

    def removeHeader(self, name: str) -> None:
        assert name is not None, "Header name must not be null"
        self.headers.remove(name)

    def getDateHeader(self, name: str) -> int:
        header: HeaderValueHolder = self.headers.get(name)
        value = None if header is None else header.getValue()
        if isinstance(value, datetime):
            return datetime.timestamp()
        elif isinstance(value, (int, float)):
            return value
        else isinstance(value, str):
            return self.parseDateHeader(name, value)
        elif value is not None:
            raise ValueError(f"Value for header '{name}' + is not a Date, Number, or String: {value}")
        else:
            return -1

    def parseDateHeader(self, name: str, value: str) -> int:
        for dateFormat in self.DATE_FORMATS:
            try:
                date = datetime.strptime(value, dateFormat)
                date = date.replace(tzinfo=self.GMT)
                return date.timestamp()
            except Exception:
                pass

        raise ValueError(f"Cannot parse date value '{value}' for '{name}' header")

    def getHeader(self, name: str) -> str:
        header: HeaderValueHolder = self.headers.get(name)
        return None if header is None else header.__str__()

    def getHeaders(self, name: str) -> list:
        header: HeaderValueHolder = self.headers.get(name)
        return [i.__str__() for i in header]

    def getHeaderNames(self) -> list:
        return list(self.headers.key())

    def getIntHeader(self, name: str) -> int:
        header: HeaderValueHolder = self.headers.get(name)
        value = None if header is None else header.getValue()
        if isinstance(value, (int, float, str)):
            return int(value)
        elif value is not None:
            raise ValueError(f"Value for header '{name}' is not a Number: {value}")
        else:
            return -1

    def setMethod(self, method: str = None) -> None:
        self.method = method

    def getMethod(self) -> str:
        return self.method

    def setPathInfo(self, pathInfo: str) -> None:
        self.pathInfo = pathInfo

    def getPathInfo(self) -> str:
        return self.pathInfo

    def getPathTranslated(self):
        return None if self.pathInfo is None else self.getRealPath(self.pathInfo)

    def setContextPath(self, contextPath: str) -> None:
        self.contextPath = contextPath

    def getContextPath(self) -> str:
        return self.contextPath

    def setQueryString(self, queryString: str = None) -> None:
        self.queryString = queryString

    def getQueryString(self) -> str:
        return self.queryString

    def setRemoteUser(self, remoteUser: str = None) -> None:
        self.remoteUser = remoteUser

    def getRemoteUser(self) -> str:
        return self.remoteUser

    def addUserRole(self, role: str) -> None:
        self.userRoles.add(role)

    def isUserInRole(self, role: str) -> bool:
        return role in self.userRoles or \
            (isinstance(MockServletContext, self.servletContext) and
                self.servletContext.getDeclaredRoles().contains(role))

    def setUserPrincipal(self, userPrincipal=None) -> None:
        self.userPrincipal = userPrincipal

    def getUserPrincipal(self):
        return self.userPrincipal

    def setRequestedSessionId(self, requestedSessionId: str = None):
        self.requestedSessionId = requestedSessionId

    def getRequestedSessionId(self) -> str:
        return self.requestedSessionId

    def setRequestURI(self, requestURI: str = None) -> None:
        self.requestURI = requestURI

    def getRequestURI(self) -> str:
        return self.requestURI

    def getRequestURL(self) -> str:
        scheme = self.getScheme()
        server = self.getServerName()
        port = self.getServerPort()
        uri = self.getRequestURI()

        url = scheme + "://" + server
        if port > 0 and \
            (self.HTTP.casefold() == scheme.casefold() and port != 80) or \
                (self.HTTPS.casefold() == scheme.casefold() and port != 443):
            url += f":{port}"
        if uri:
            url += uri
        return url

    def setServletPath(self, servletPath: str) -> None:
        self.servletPath = servletPath

    def getServletPath(self) -> str:
        return self.servletPath

    # return type HttpSession
    def setSession(self, session):
        self.session = session
        if isinstance(session, MockHttpSession):
            session.access()

    def getSession(self, create: bool = True):
        self.checkActive()
        if isinstance(session, MockHttpSession) and self.session.isInvalid():
            self.session = None
        if self.session is None and create:
            self.session = MockHttpSession(self.servletContext)
        return self.session

    def changeSessionId(self) -> str:
        assert self.session is not None, "The request does not have a session"
        if isinstance(session, MockHttpSession):
            return self.session.changeSessionId()
        return self.session.getId()

    def setRequestedSessionIdValid(self, requestedSessionIdValid: bool) -> None:
        self.requestedSessionIdValid = requestedSessionIdValid

    def isRequestedSessionIdValid(self) -> bool:
        return self.isRequestedSessionIdValid

    def setRequestedSessionIdFromCookie(self, requestedSessionIdFromCookie) -> None:
        self.requestedSessionIdFromCookie = requestedSessionIdFromCookie

    def isRequestedSessionIdFromCookie(self) -> bool:
        return self.isRequestedSessionIdFromCookie

    def setRequestedSessionIdFromURL(self, requestedSessionIdFromURL: bool) -> None:
        self.requestedSessionIdFromURL = requestedSessionIdFromURL

    def isRequestedSessionIdFromURL(self) -> bool:
        return self.isRequestedSessionIdFromURL

    def isRequestedSessionIdFromUrl(self) -> bool:
        return isRequestedSessionIdFromURL()

    def authenticate(self, response) -> bool:
        raise ValueError("UnsupportedOperationException")

    def logout(self) -> None:
        self.userPrincipal = None
        self.remoteUser = None
        self.authType = None

    def addPart(self, part) -> None:
        self.parts.add(part.getName(), part)

    # return type Part
    def getPart(self, name: str):
        tmp = list(self.parts.keys())
        if tmp:
            return tmp[0]
        return None

    def getParts(self) -> set:
        result = []
        for part_list in self.parts.values():
            result.extend(part_list)
        return result

    def upgrade(self):
        raise ValueError("UnsupportedOperationException")
