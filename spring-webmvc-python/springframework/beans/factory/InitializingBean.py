from abc import ABC, ABCMeta, abstractmethod


class InitializingBean(ABC):

    @abstractmethod
    def after_properties_set(self):
        raise NotImplementedError