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
    def getContentType() -> str:
        return None
    def render(model: dict, request: HttpServletRequest, response: HttpServletResponse) -> None:
        pass
    _UNRESOLVED_VIEW = type('view', View, {'getContentType': getContentType, 'render': render})

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
    def setCacheLimit(cacheLimit: int) -> None:
        self.cacheLimit = cacheLimit

    # Return the maximum number of entries for the view cache.
    def getCacheLimit() -> int:
        return self.cacheLimit

    # Enable or disable caching.
    # Disable this only for debugging and development.
    def setCache(cache: bool) -> None:
        self.cacheLimit = (cache ? DEFAULT_CACHE_LIMIT : 0)

    # Return if caching is enabled.
    def isCache() -> bool:
        return (self.cacheLimit > 0)

    def setCacheUnresolved(cacheUnresolved: bool) -> None:
        self.cacheUnresolved = cacheUnresolved

    # Return if caching of unresolved views is enabled.
    def isCacheUnresolved() -> bool:
        return self.cacheUnresolved

    def setCacheFilter(cacheFilter: CacheFilter) -> None:
        assert cacheFilter != None
        self.cacheFilter = cacheFilter

    def getCacheFilter() -> CacheFilter:
        return self.cacheFilter

    def resolveViewName(viewName: str, locale: Locale) -> View:
        if (not isCache()):
            return createView(viewName, locale)

        else:
            cacheKey = getCacheKey(viewName, locale)
            view = self.viewAccessCache.get(cacheKey)
            if (view == None):
                with lock:
                    view = self.viewCreationCache.get(cacheKey)
                    if (view == None):
                        # Ask the subclass to create the View object.
                        view = createView(viewName, locale)
                        if (view == None and self.cacheUnresolved):
                            view = UNRESOLVED_VIEW
                        
                        if (view != None and self.cacheFilter.filter(viewName, locale)):
                            self.viewAccessCache[cacheKey] = view
                            self.viewCreationCache[cacheKey] = view

            return (view if view != UNRESOLVED_VIEW else None)
    
    def _formatKey(cacheKey: object) -> str:
        return "View with key [" + cacheKey + "] "

    def getCacheKey(viewName: str, locale: Locale) -> object:
        return viewName + '_' + locale

    def removeFromCache(viewName: str, locale: Locale) -> None:
        if isCache():
            cacheKey = getCacheKey(viewName, locale)
            with lock:
                self.viewAccessCache.pop(cacheKey, None)
                cachedView = self.viewCreationCache.pop(cacheKey, None)

    def clearCache() -> None:
        with lock:
            self.viewAccessCache = dict()
            self.viewCreationCache = dict()

    def createView(viewName: str, locale: Locale) -> View:
        return loadView(viewName, locale)

    @abstractmethod
    def loadView(viewName: str, locale: Locale) -> View:
        pass

    class CacheFilter():
        def filter(view, viewName, locale):
            pass
            
