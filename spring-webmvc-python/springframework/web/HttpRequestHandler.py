from abc import ABC, abstractmethod
from springframework.utils.mock.inst import HttpServletRequest
from springframework.utils.mock.inst import HttpServletResponse


class HttpRequestHandler(ABC):

    @abstractmethod
    def handleRequest(
        self,
        request: HttpServletRequest,
        response: HttpServletResponse
    ) -> None:
        pass
