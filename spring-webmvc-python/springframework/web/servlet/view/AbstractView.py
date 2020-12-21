from unittest import mock
import logging
from abc import abstractmethod, ABC

from web.context.support.WebApplicationObjectSupport import WebApplicationObjectSupport
from beans.factory.BeanNameAware import BeanNameAware
from springframework.web.servlet.View import View

# mock objects
RequestContext = mock.MagicMock()
RequestContext.configure_mock(name='RequestContext')
ContextExposingHttpServletRequest = mock.MagicMock()
ContextExposingHttpServletRequest.configure_mock(name='ContextExposingHttpServletRequest')
mediaType = mock.MagicMock()
mediaType.configure_mock(name="mediaType")


class AbstractView(WebApplicationObjectSupport, View, BeanNameAware, ABC):
    DEFAULT_CONTENT_TYPE = "text/html;charset=ISO-8859-1"
    OUTPUT_BYTE_ARRAY_INITIAL_SIZE = 4096
    contentType = DEFAULT_CONTENT_TYPE
    staticAttributes = dict()
    exposePathVariables = dict()
    exposeContextBeansAsAttributes = False
    exposedContextBeanNames = set()

    def setContentType(self, contentType: str = None) -> None:
        self.contentType = contentType

    def getContentType(self) -> str:
        return self.contentType

    def setRequestContextAttribute(self, requestContextAttribute: str) -> None:
        self.requestContextAttribute = requestContextAttribute

    def getRequestContextAttribute(self) -> str:
        return self.requestContextAttribute

    def setAttributesCSV(self, propString: str = None) -> None:
        if propString is not None:
            token_list = propString.split(',')
            for token in token_list:
                if "=" not in token:
                    raise ValueError("Expected '=' in attributes CSV string '" + propString + "'")
                if token.index("=") >= (len(token) - 2):
                    raise ValueError(
                        "At least 2 characters ([]) required in attributes CSV string '" + propString + "'")
                name, value = token.split("=")
                self.addStaticAttribute(name, value)

    def setAttributes(self, attributes: dict) -> None:
        self.staticAttributes.update(attributes)

    def setAttributesMap(self, attributes: dict = None) -> None:
        if attributes is not None:
            for name in attributes:
                value = attributes[name]
                self.addStaticAttribute(name, value)

    def getAttributesMap(self) -> dict:
        return self.staticAttributes

    def addStaticAttribute(self, name: str, value) -> None:
        self.staticAttributes[name] = value

    def getStaticAttributes(self) -> dict:
        return self.staticAttributes.copy()

    def isExposePathVariables(self) -> bool:
        return self.exposePathVariables

    def setExposeContextBeansAsAttributes(self, exposeContextBeansAsAttributes: bool) -> None:
        self.exposeContextBeansAsAttributes = exposeContextBeansAsAttributes

    def setExposedContextBeanNames(self, exposedContextBeanNames: list) -> None:
        self.exposedContextBeanNames = set(exposedContextBeanNames)

    def setBeanName(self, beanName: str) -> None:
        self.beanName = beanName

    def getBeanName(self) -> str:
        return self.beanName

    def render(self, model: dict, request, response) -> None:
        logging.debug(
            "View " +
            self.formatViewName() +
            ", model " +
            str((dict() if model is None else model)) +
            str((", static attributes " + self.staticAttributes if self.staticAttributes else ""))
        )
        mergedModel = self.createMergedOutputModel(model, request, response)
        self.prepareResponse(request, response)
        self.renderMergedOutputModel(mergedModel, self.getRequestToExpose(request), response)

    def createMergedOutputModel(self, model: dict, request, response) -> dict:
        pathVars = None
        if self.exposePathVariables:
            pathVars = request.getAttribute(View.PATH_VARIABLES)

        size = len(self.staticAttributes)
        size += len(model)
        size += len(pathVars)

        mergedModel = dict()
        mergedModel.update(self.staticAttributes)
        mergedModel.update(pathVars)
        mergedModel.update(model)

        # Expose RequestContext?
        if self.requestContextAttribute is not None:
            value = self.createRequestContext(request, response, mergedModel)
            mergedModel[self.requestContextAttribute] = value

        return mergedModel

    def createRequestContext(self, request, response, model: dict) -> RequestContext:
        # RequestContext use mock
        return RequestContext(request, response, self.getServletContext(), model)

    def prepareResponse(self, request, response) -> None:
        if self.generatesDownloadContent():
            response.setHeader("Pragma", "private")
            response.setHeader("Cache-Control", "private, must-revalidate")

    def generatesDownloadContent(self) -> bool:
        return False

    # return type : HttpServletRequest
    def getRequestToExpose(self, originalRequest):
        if self.exposeContextBeansAsAttributes or self.exposedContextBeanNames is not None:
            # wac = getWebApplicationContext()
            wac = self.get_web_application_context()
            assert wac is not None, "No WebApplicationContext"
            # ContextExposingHttpServletRequest use mock
            return ContextExposingHttpServletRequest(originalRequest, wac, self.exposedContextBeanNames)
        return originalRequest

    @abstractmethod
    def renderMergedOutputModel(self, model: dict, request, response):
        raise NotImplementedError

    def exposeModelAsRequestAttributes(self, model: dict, request):
        for name, value in model.items():
            # make sure request has this method
            if value is not None:
                request.setAttribute(name, value)
            else:
                request.removeAttribute(name)

    def createTemporaryOutputStream(self) -> bytearray:
        return bytearray(self.OUTPUT_BYTE_ARRAY_INITIAL_SIZE)

    def writeToResponse(self, response, baos: bytearray):
        # Write content type and also length (determined via byte array).
        response.setContentType(self.getContentType())
        response.setContentLength(baos.size())

        # Flush byte array to servlet output stream.
        out = response.getOutputStream()
        baos.writeTo(out)
        out.flush()

    def setResponseContentType(self, request, response) -> None:
        # mediaType use mock
        mediaType = request.getattr(View.SELECTED_CONTENT_TYPE)
        if mediaType is not None and mediaType.isConcrete():
            response.setContentType(mediaType.toString())
        else:
            response.setContentType(self.getContentType())

    def toString(self) -> str:
        return self.__class__.__qualname__ + ": " + self.formatViewName()

    def formatViewName(self) -> str:
        if self.getBeanName() is not None:
            return "name '" + self.getBeanName() + "'"
        else:
            return "[" + self.__class__.__name__ + "]"
