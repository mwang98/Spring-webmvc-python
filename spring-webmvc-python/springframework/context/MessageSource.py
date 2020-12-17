from abc import ABC, ABCMeta, abstractmethod
from springframework.function.support.multiple import MultipleMeta
from typing import List


class MessageSource(ABC, MultipleMeta):
    @abstractmethod
    def get_message(self, code: str, args: List[object], default_message: str, locale: Locale):
        raise NotImplementedError

    # TODO: function overloading issue
