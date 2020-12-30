from abc import ABC

from springframework.utils.mock.inst import HttpServletRequest

class LastModified(ABC):

    @abstractmethod
    def get_last_modified(request: HttpServletRequest) -> int:
        raise NotImplementedError