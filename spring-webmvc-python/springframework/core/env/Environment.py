from abc import ABC, abstractmethod
from typing import List
from springframework.core.env.Profiles import Profiles

from springframework.core.env.Profiles import Profiles
from springframework.core.env.PropertyResolver import PropertyResolver


class Environment(PropertyResolver, ABC):
    @abstractmethod
    def get_active_profiles(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def get_default_profiles(self) -> List[str]:
        raise NotImplementedError

    @abstractmethod
    def accepts_profiles(self, profiles: Profiles) -> bool:
        raise NotImplementedError
