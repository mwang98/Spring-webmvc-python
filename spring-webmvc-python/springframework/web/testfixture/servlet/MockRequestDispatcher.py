import logging
from springframework.utils.mock.type import HttpServletResponseWrapper

from .MockHttpServletResponse import MockHttpServletResponse


class MockRequestDispatcher():

    logger = logging.getLogger()
    resource: str = None

    def __init__(self, resource: str):
        assert resource is not None, "Resource must not be null"
        self.resource = resource

    def forward(self, request, response) -> None:
        assert request is not None, "Request must not be null"
        assert response is not None, "Response must not be null"
        assert not response.isCommitted(), "Cannot perform forward - response is already committed"
        self.getMockHttpServletResponse(response).setForwardedUrl(self.resource)

    def include(self, request, response) -> None:
        assert request is not None, "Request must not be null"
        assert response is not None, "Response must not be null"
        self.getMockHttpServletResponse(response).addIncludedUrl(self.resource);
        self.logger.debug(f"MockRequestDispatcher: including [ {self.resource} ]")

    def getMockHttpServletResponse(self, response):
        if isinstance(response, MockHttpServletResponse):
            return response
        if isinstance(response, HttpServletResponseWrapper):
            return self.getMockHttpServletResponse(response.getResponse())
        raise ValueError("MockRequestDispatcher requires MockHttpServletResponse")
