from abc import ABC, abstractmethod
from typing import List

class Environment(PropertyResolver):
    @abstractmethod
    def get_active_profiles(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_default_profiles(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def accepts_profiles(self, profiles: Profiles) -> bool:
        raise NotImplementedError
