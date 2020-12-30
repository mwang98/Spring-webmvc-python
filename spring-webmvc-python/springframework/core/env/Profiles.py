from abc import ABC, abstractmethod

from env.ProfilesParser import ProfilesParser


class Profiles(ABC):
    @abstractmethod
    def matches(self, active_profiles) -> bool:
        raise NotImplementedError

    @classmethod
    def of(cls, *profiles):
        return ProfilesParser.parse(profiles)
