from abc import ABC

from springframework.web.servlet.view.AbstractView import AbstractView
from springframework.beans.factory.InitializingBean import InitializingBean


class AbstractUrlBasedView(AbstractView, InitializingBean, ABC):
    url: str = None

    def __init__(self, url: str):
        super().__init__()
        self.url = url

    def setUrl(self, url: str) -> None:
        self.url = url

    def getUrl(self) -> str:
        return self.url

    def afterPropertiesSet(self) -> None:
        if self.isUrlRequired() and self.getUrl() is None:
            raise ValueError("Property 'url' is required")

    def isUrlRequired(self) -> bool:
        return True

    def checkResource(self, locale) -> bool:
        # local type: Locale
        return True

    def toString(self) -> str:
        return super().toString() + f"; URL [{self.getUrl()}]"
