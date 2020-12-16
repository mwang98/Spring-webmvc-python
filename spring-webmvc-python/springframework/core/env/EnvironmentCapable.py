from abc import ABC, abstractmethod


class EnvironmentCapable(ABC):
    @abstractmethod
    def get_environment(self) -> Environment:
        raise NotImplementedError
