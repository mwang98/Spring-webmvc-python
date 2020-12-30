import logging
from springframework.web.servlet.handler import AbstractUrlHandlerMapping


class SimpleUrlHandlerMapping(AbstractUrlHandlerMapping):

    def __init__(self, urlMap: dict = None, order: int = None):
        self.urlMap = dict()
        if isinstance(urlMap, dict):
            self.setUrlMap(urlMap)
        if isinstance(order, int):
            self.setOrder(order)

    def setMappings(self, mappings: dict) -> None:
        self.urlMap.update(mappings)

    def setUrlMap(self, urlMap: dict) -> None:
        self.urlMap.update(urlMap)

    def getUrlMap(self) -> dict:
        return self.urlMap

    def initApplicationContext(self) -> None:
        super().initApplicationContext()
        self.registerHandlers(self.urlMap)

    def registerHandlers(self, urlMap: dict) -> None:
        if not urlMap:
            logging.info(f"No patterns in {self.formatMappingName()}")
        else:
            for url, handler in urlMap.items():
                # Prepend with slash if not already present.
                if not url.startswith('/'):
                    url = '/' + url
                # Remove whitespace from handler bean name.
                if isinstance(handler, str):
                    handler = handler.strip()
                self.registerHandlers(url, handler)

            patterns = list()
            if self.getRootHandler() is not None:
                patterns.append('/')
            if self.getDefaultHandler() is not None:
                patterns.append('/**')
            patterns.extend(list(self.getHandlerMap().keys()))
            logging.debug(f"Patterns {patterns} in {self.formatMappingName()}")
