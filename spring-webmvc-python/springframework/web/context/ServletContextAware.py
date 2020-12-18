from springframework.beans.factory import Aware
from abc import ABC, abstractmethod


class ServletContextAware(Aware, ABC):
    @abstractmethod
    def set_servlet_context(self, servlet_context: ServletContext):
        raise NotImplementedError
