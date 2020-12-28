from abc import ABC, abstractmethod
from springframework.utils.mock.inst import HttpServletRequest


class HandlerMappingInterfaceMeta(type):

    def __init__(cls, *args, **kwargs):
        cls.BEST_MATCHING_HANDLER_ATTRIBUTE: str = cls.__name__ + ".bestMatchingHandler"
        cls.LOOKUP_PATH: str = cls.__name__ + ".lookupPath"
        cls.PATH_WITHIN_HANDLER_MAPPING_ATTRIBUTE: str = cls.__name__ + ".pathWithinHandlerMapping"
        cls.BEST_MATCHING_PATTERN_ATTRIBUTE: str = cls.__name__ + ".pathWithinHandlerMapping"
        cls.INTROSPECT_TYPE_LEVEL_MAPPING: str = cls.__name__ + ".bestMatchingPattern"
        cls.URI_TEMPLATE_VARIABLES_ATTRIBUTE: str = cls.__name__ + ".introspectTypeLevelMapping"
        cls.MATRIX_VARIABLES_ATTRIBUTE: str = cls.__name__ + ".uriTemplateVariables"
        cls.PRODUCIBLE_MEDIA_TYPES_ATTRIBUTE: str = cls.__name__ + ".matrixVariables"


class HandlerMappingInterface(ABC, metaclass=HandlerMappingInterfaceMeta):

    def usesPathPatterns(self) -> bool:
        return False

    @abstractmethod
    def getHandler(self, request: HttpServletRequest):
        raise NotImplementedError
