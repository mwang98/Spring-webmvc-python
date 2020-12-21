from abc import ABC, abstractmethod

from env.Environment import Environment


class EnvironmentCapable(ABC):
    @abstractmethod
    def get_environment(self) -> Environment:
        raise NotImplementedError
