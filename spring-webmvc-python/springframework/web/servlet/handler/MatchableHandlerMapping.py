from abc import ABC, abstractclassmethod
from springframework.web.util.pattern import PathPatternParser
from springframework.web.servlet.handler import RequestMatchResult
from springframework.utils.mock.inst import HttpServletRequest


class MatchableHandlerMapping(ABC, HandlerMapping):

    def get_pattern_parser(self) -> PathPattern:
        return None

    @abstractmethod
    def match(self, request: HttpServletRequest, pattern: str) -> RequestMatchResult:
        return None
    
