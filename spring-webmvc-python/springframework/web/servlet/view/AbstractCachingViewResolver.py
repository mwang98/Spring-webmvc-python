from abc import abstractmethod, ABC
import threading

from mock.inst import Locale
from context.support.WebApplicationObjectSupport import WebApplicationObjectSupport
from springframework.web.servlet import View
from springframework.web.servlet import ViewResolver

class AbstractCachingViewResolver(WebApplicationObjectSupport, ViewResolver, ABC):
    
    # Default maximum number of entries for the view cache: 1024.
	DEFAULT_CACHE_LIMIT = 1024

    lock = threading.Lock()

    # Dummy marker object for unresolved views in the cache Maps.
    def getContentType(self) -> str:
        return None
    def render(self, model: dict, request: HttpServletRequest, response: HttpServletResponse) -> None:
        pass
    _UNRESOLVED_VIEW = type('view', View, {'getContentType': AbstractCachingViewResolver.getContentType, 'render': render})

    # Default cache filter that always caches.
    # todo 
    # private static final CacheFilter DEFAULT_CACHE_FILTER = (view, viewName, locale) -> true;
    # _DEFAULT_CACHE_FILTER = (view, viewName, locale)

    # The maximum number of entries in the cache.
    _cacheLimit = DEFAULT_CACHE_LIMIT

    # Whether we should refrain from resolving views again if unresolved once.
    _cacheUnresolved = True

    # Filter function that determines if view should be cached.
    _cacheFilter = _DEFAULT_CACHE_FILTER

    # Fast access cache for Views, returning already cached instances without a global lock.
    _viewAccessCache = dict.fromkeys(range(DEFAULT_CACHE_LIMIT))

    # Map from view key to View instance, synchronized for View creation.
    _viewCreationCache = dict.fromkeys(range(DEFAULT_CACHE_LIMIT), 0.75, True):
    # todo

    #Specify the maximum number of entries for the view cache.
    #Default is 1024.
    def setCacheLimit(self, cacheLimit: int) -> None:
        self.cacheLimit = cacheLimit

    # Return the maximum number of entries for the view cache.
    def getCacheLimit(self) -> int:
        return self.cacheLimit

    # Enable or disable caching.
    # Disable this only for debugging and development.
    def setCache(self, cache: bool) -> None:
        self.cacheLimit = (DEFAULT_CACHE_LIMIT if cache else 0)

    # Return if caching is enabled.
    def isCache(self) -> bool:
        return (self.cacheLimit > 0)

    def setCacheUnresolved(self, cacheUnresolved: bool) -> None:
        self.cacheUnresolved = cacheUnresolved

    # Return if caching of unresolved views is enabled.
    def isCacheUnresolved(self) -> bool:
        return self.cacheUnresolved

    def setCacheFilter(self, cacheFilter: CacheFilter) -> None:
        assert cacheFilter is not None
        self.cacheFilter = cacheFilter

    def getCacheFilter(self) -> CacheFilter:
        return self.cacheFilter

    def resolveViewName(self, viewName: str, locale: Locale) -> View:
        if (not isCache()):
            return self.createView(viewName, locale)

        else:
            cacheKey = self.getCacheKey(viewName, locale)
            view = self.viewAccessCache.get(cacheKey)
            if (view == None):
                with lock:
                    view = self.viewCreationCache.get(cacheKey)
                    if (view == None):
                        # Ask the subclass to create the View object.
                        view = self.createView(viewName, locale)
                        if (view == None and self.cacheUnresolved):
                            view = self._UNRESOLVED_VIEW
                        
                        if (view != None and self.cacheFilter.filter(viewName, locale)):
                            self.viewAccessCache[cacheKey] = view
                            self.viewCreationCache[cacheKey] = view

            return (view if view != self._UNRESOLVED_VIEW else None)
    
    def _formatKey(self, cacheKey: object) -> str:
        return "View with key [" + cacheKey + "] "

    def getCacheKey(self, viewName: str, locale: Locale) -> object:
        return viewName + '_' + locale

    def removeFromCache(self, viewName: str, locale: Locale) -> None:
        if isCache():
            cacheKey = self.getCacheKey(viewName, locale)
            with self.lock:
                self.viewAccessCache.pop(cacheKey, None)
                cachedView = self.viewCreationCache.pop(cacheKey, None)

    def clearCache(self) -> None:
        with self.lock:
            self.viewAccessCache = dict()
            self.viewCreationCache = dict()

    def createView(self, viewName: str, locale: Locale) -> View:
        return self.loadView(viewName, locale)

    @abstractmethod
    def loadView(self, viewName: str, locale: Locale) -> View:
        pass

    class CacheFilter():
        def filter(self, view, viewName, locale):
            pass
            
