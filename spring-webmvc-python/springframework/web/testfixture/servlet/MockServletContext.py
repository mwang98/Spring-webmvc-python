import os
import logging
import tempfile
from springframework.utils.mock.inst import SessionTrackingMode, \
    DefaultResourceLoader, MediaTypeFactory, MediaType, Resource, RequestDispatcher


from springframework.utils.mock.inst import SessionCookieConfig as MockSessionCookieConfig
from springframework.utils.mock.inst import RequestDispatcher as MockRequestDispatcher
# from .MockSessionCookieConfig import MockSessionCookieConfig
# from .MockRequestDispatcher import MockRequestDispatcher


class MockServletContext():

    COMMON_DEFAULT_SERVLET_NAME: str = "default"
    TEMP_DIR_SYSTEM_PROPERTY: str = tempfile.gettempdir()
    DEFAULT_SESSION_TRACKING_MODES = set([
        SessionTrackingMode.COOKIE,
        SessionTrackingMode.URL,
        SessionTrackingMode.SSL
    ])

    logger = logging.getLogger()
    resourceLoader = None
    resourceBasePath: str = None
    contextPath: str = ""
    contexts = dict()
    majorVersion: int = 3
    minorVersion: int = 1
    effectiveMajorVersion: int = 3
    effectiveMinorVersion: int = 1
    namedRequestDispatchers = dict()
    defaultServletName: str = COMMON_DEFAULT_SERVLET_NAME
    initParameters = dict()
    attributes = dict()
    servletContextName: str = "MockServletContext"
    declaredRoles = set()
    sessionTrackingModes: set = None
    sessionCookieConfig = MockSessionCookieConfig()
    sessionTimeout: int = None
    requestCharacterEncoding: str = None
    responseCharacterEncoding: str = None
    mimeTypes = dict()

    def __init__(self, resourceBasePath: str, resourceLoader=None) -> None:
        if resourceLoader is None:
            self.resourceLoader = DefaultResourceLoader()
        else:
            self.resourceLoader = resourceLoader
        self.registerNamedDispatcher(self.defaultServletName, MockRequestDispatcher(self.defaultServletName))

    def getResourceLocation(self, path: str) -> str:
        if not path.startswith('/'):
            path = "/" + path
        return self.resourceBasePath + path

    def setContextPath(self, contextPath: str) -> None:
        self.contextPath = contextPath

    def getContextPath(self) -> str:
        return self.contextPath

    def registerContext(self, contextPath: str, context) -> None:
        self.contexts[contextPath] = context

    def getContext(self, contextPath: str):
        if self.contextPath == contextPath:
            return contextPath
        return self.contexts.get(contextPath)

    def setMajorVersion(self, majorVersion: int):
        self.majorVersion = majorVersion

    def getMajorVersion(self) -> int:
        return self.majorVersion

    def setMinorVersion(self, minorVersion: int) -> None:
        self.minorVersion = minorVersion

    def getMinorVersion(self) -> int:
        return self.minorVersion

    def setEffectiveMajorVersion(self, effectiveMajorVersion: int) -> None:
        self.effectiveMajorVersion = effectiveMajorVersion

    def getEffectiveMajorVersion(self) -> int:
        return self.effectiveMajorVersion

    def getMimeType(self, filePath: str) -> str:
        filename, extension = os.path.splitext(filePath)
        if extension in self.mimeTypes:
            return str(self.mimeTypes.get(extension))
        else:
            return str(MediaTypeFactory.getMediaType(filePath))

    def addMimeType(self, fileExtension: str, mimeType: MediaType) -> None:
        assert fileExtension is not None, "'fileExtension' must not be null"
        self.mimeTypes[fileExtension] = mimeType

    def getResourcePaths(self, path: str) -> set:
        actualPath = path if path.endswith("/") else path + '/'
        resourceLocation = self.getResourceLocation(actualPath)
        resource: Resource = None
        try:
            resource = self.resourceLoader.getResource(resourceLocation)
            file = resource.getFile()
            fileList = file.list()
            if not fileList:
                return None
            resourcePaths = set()
            for fileEntry in fileList:
                resultPath = actualPath + fileEntry
                if resource.createRelative(fileEntry).getFile().isDirectory():
                    resultPath += "/"
                resourcePaths.add(resultPath)
            return resourcePaths

        except IOError as e:
            resource = resource if resource is not None else resourceLocation
            self.logger.warning(f"Could not get resource paths for {resource}. {str(e)}")
            return None

    def getResource(self, path: str):
        resourceLocation = self.getResourceLocation(path)
        resource: Resource = None
        try:
            resource = self.resourceLoader.getResource(resourceLocation)
            if not resource.exists():
                return None
            return resource.getURL()
        except IOError as e:
            resource = resource if resource is not None else resourceLocation
            self.logger.warning(f"Could not get URL for resource {resource}. {str(e)}")
            return None

    def getResourceAsStream(self, path: str):
        resourceLocation = self.getResourceLocation(path)
        resource: Resource = None
        try:
            resource = self.resourceLoader.getResource(resourceLocation)
            if not resource.exists():
                return None
            return resource.getInputStream()
        except IOError as e:
            resource = resource if resource is not None else resourceLocation
            self.logger.warning(f"Could not get URL for resource {resource}. {str(e)}")
            return None

    def getRequestDispatcher(self, path: str) -> RequestDispatcher:
        assert path.startswith('/'), f"RequestDispatcher path [ {path} ] at ServletContext level must start with '/'"
        return MockRequestDispatcher(path)

    def getNamedDispatcher(self, path: str) -> RequestDispatcher:
        return self.namedRequestDispatchers.get(path)

    def registerNamedDispatcher(self, name: str, requestDispatcher: RequestDispatcher) -> None:
        assert name is not None, "RequestDispatcher name must not be null"
        assert requestDispatcher is not None, "RequestDispatcher must not be null"
        self.namedRequestDispatchers[name] = requestDispatcher

    def unregisterNamedDispatcher(self, name: str) -> None:
        assert name is not None, "RequestDispatcher name must not be null"
        self.namedRequestDispatchers.pop(name)

    def getDefaultServletName(self) -> str:
        return self.defaultServletName

    def setDefaultServletName(self, defaultServletName: str):
        assert defaultServletName, "defaultServletName must not be null or empty"
        self.unregisterNamedDispatcher(self.defaultServletName)
        self.defaultServletName = defaultServletName
        self.registerNamedDispatcher(defaultServletName, MockRequestDispatcher(defaultServletName))

    def getServlet(self, name: str):
        return None

    def getServlets(self) -> list:
        return list()

    def getServletNames(self) -> list:
        return list()

    def log(self, message: str) -> None:
        self.logger.info(message)

    def getRealPath(self, path: str) -> str:
        resourceLocation = self.getResourceLocation(path)
        resource: Resource = None
        try:
            resource = self.resourceLoader.getResource(resourceLocation)
            return resource.getFile().getAbsolutePath()
        except IOError as e:
            resource = resource if resource is not None else resourceLocation
            self.logger.warning(f"Could not determine real path of resource {resource}. {str(e)}")
            return None

    def getServerInfo(self) -> str:
        return "MockServletContext"

    def getInitParameter(self, name: str) -> str:
        assert name is not None, "Parameter name must not be null"
        return self.initParameters.get(name)

    def getInitParameterNames(self) -> list:
        return list(self.initParameters.keys())

    def setInitParameter(self, name: str, value: str) -> bool:
        assert name is not None, "Parameter name must not be null"
        if name in self.initParameters:
            return False
        self.initParameters[name] = value
        return True

    def addInitParameter(self, name: str, value: str) -> None:
        assert name is not None, "Parameter name must not be null"
        self.initParameters[name] = value

    def getAttribute(self, name: str):
        assert name is not None, "Attribute name must not be null"
        return self.attributes.get(name)

    def getAttributeNames(self) -> list:
        return list(self.attributes.keys())

    def setAttribute(self, name: str, value=None) -> None:
        assert name is not None, "Attribute name must not be null"
        if value is not None:
            self.attributes[name] = value
        else:
            self.attributes.pop(name)

    def removeAttribute(self, name: str) -> None:
        assert name is not None, "Attribute name must not be null"
        self.attributes.pop(name)

    def setServletContextName(self, servletContextName: str) -> None:
        self.servletContextName = servletContextName

    def getServletContextName(self) -> str:
        return self.getServletContextName

    def getClassLoader(self):
        # TODO
        assert False

    def declareRoles(self, roleNames: list) -> None:
        assert roleNames is not None, "Role names array must not be null"
        for roleName in roleNames:
            assert roleName, "Role name must not be empty"
            self.declaredRoles.add(roleName)

    def getDeclaredRoles(self) -> set:
        return set(self.declaredRoles).copy()

    def setSessionTrackingModes(self, sessionTrackingModes: set) -> None:
        self.sessionTrackingModes = sessionTrackingModes

    def getDefaultSessionTrackingModes(self) -> set:
        return self.DEFAULT_SESSION_TRACKING_MODES

    def getEffectiveSessionTrackingModes(self) -> set:
        if self.sessionTrackingModes is None:
            return self.DEFAULT_SESSION_TRACKING_MODES
        return self.sessionTrackingModes

    def getSessionCookieConfig(self):
        return self.sessionCookieConfig

    def setSessionTimeout(self, sessionTimeout: int) -> None:
        self.sessionTimeout = sessionTimeout

    def getSessionTimeout(self) -> int:
        return self.sessionTimeout

    def setRequestCharacterEncoding(self, requestCharacterEncoding: str = None) -> None:
        self.requestCharacterEncoding = requestCharacterEncoding

    def getRequestCharacterEncoding(self) -> str:
        self.requestCharacterEncoding

    def setResponseCharacterEncoding(self, responseCharacterEncoding: str = None) -> None:
        self.responseCharacterEncoding = responseCharacterEncoding

    def getResponseCharacterEncoding(self) -> str:
        return self.getResponseCharacterEncoding

    # ---------------------------------------------------------------------
    #  Unsupported Servlet 3.0 registration methods
    # ---------------------------------------------------------------------
    # TODO
