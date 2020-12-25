from abc import abstractmethod, ABC
from springframework.web.servlet import View
from mock.inst import Locale


class ViewResolver(ABC):
    def resolve_view_name(self, viewName: str, locale: Locale) -> View:
        raise NotImplementedError
