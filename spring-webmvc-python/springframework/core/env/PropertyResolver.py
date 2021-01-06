from abc import ABC, abstractmethod
from typing import TypeVar, ClassVar
from springframework.function.support.overload import overload

T = TypeVar('T')


class PropertyResolver(ABC):
    @abstractmethod
    def contains_property(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    @overload
    def get_property(self, key: str, default_value: str = None) -> str:
        raise NotImplementedError

    @abstractmethod
    @overload
    def get_property(
        self,
        key: str,
        target_type: ClassVar[T],
        defaultValue: T
    ) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_required_property(self, key: str, target_type: ClassVar[T]):
        raise NotImplementedError

    @abstractmethod
    def resolve_placeholders(self, text: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def resolve_required_placeholders(self, text: str) -> str:
        raise NotImplementedError
