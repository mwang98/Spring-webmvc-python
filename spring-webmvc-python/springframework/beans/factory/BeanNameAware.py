from abc import ABC, ABCMeta, abstractmethod


class BeanNameAware(ABC):

    @abstractmethod
    def set_bean_name(self, name: str) -> None:
        raise NotImplementedError
