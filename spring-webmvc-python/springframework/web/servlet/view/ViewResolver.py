from abc import abstractmethod, ABC
from springframework.web.servlet import View

class ViewResolver(ABC):
    # todo (Locale)
    def resolveViewName(viewName, locale) -> View:
        raise NotImplementedError
