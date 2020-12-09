from ..beans.factory import Aware
from abc import ABC, ABCMeta, abstractmethod


class ApplicationContextAware(metaclass=Aware):
    @abstractmethod
    def set_application_context(self, application_context: ApplicationContext):
        raise NotImplementedError
