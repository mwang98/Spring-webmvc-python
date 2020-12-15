from .MockServletContext import MockServletContext


# inherit from ServletConfigInterface
class MockServletConfig():

    initParameters = dict()

    def __init__(self, servletName: str = "", servletContext=None):
        self.servletName = servletName
        if servletContext is None:
            self.servletContext = MockServletContext()
        else:
            self.servletContext = servletContext

    def getServletName(self) -> str:
        return self.servletName

    def getServletContext(self) -> str:
        return self.servletContext

    def addInitParameter(self, name: str, value: str) -> None:
        assert name is not None, "Parameter name must not be null"
        self.initParameters[name] = value

    def getInitParameter(self, name: str) -> str:
        return self.initParameters.get(name)

    def getInitParameterNames(self) -> list:
        return self.initParameters.keys()
