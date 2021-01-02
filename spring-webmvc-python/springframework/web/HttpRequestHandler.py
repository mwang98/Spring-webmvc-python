from abc import ABC, abstractmethod
from springframework.utils.mock.inst import HttpServletRequest, HttpServletResponse


class HttpRequestHandler(ABC):

    @abstractmethod
    def handleRequest(self, request: HttpServletRequest, response: HttpServletResponse) -> None:
        pass
    