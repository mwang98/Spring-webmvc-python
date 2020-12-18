from abc import ABC, abstractmethod
from typing import List

from mock.inst import Locale


class MessageSource(ABC):
    @abstractmethod
    def get_message(self, locale: Locale, default_message: str = None, resolvable: MessageSourceResolvable = None,
                    code: str = None, args: List[object] = None):
        raise NotImplementedError
