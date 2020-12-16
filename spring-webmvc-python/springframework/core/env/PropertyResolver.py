from abc import ABC, abstractmethod
from typing import TypeVar, ClassVar

T = TypeVar('T')
class PropertyResolver(ABC):
    @abstractmethod
    def contains_property(self, key: str) -> bool:
        raise NotImplementedError

    @abstractmethod
    def get_property(self, key: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_property(self, key: str, default_value: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def get_property(self, key: str, target_type: ClassVar[T]) -> T:
        raise NotImplementedError

    @abstractmethod
    def get_required_property(self, key: str, target_type):
        raise NotImplementedError

    @abstractmethod
    def resolve_placeholders(self, text: str) -> str:
        raise NotImplementedError

    @abstractmethod
    def resolve_required_placeholders(self, text: str) -> str:
        raise NotImplementedError