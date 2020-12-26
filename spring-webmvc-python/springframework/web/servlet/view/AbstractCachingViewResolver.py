from abc import abstractmethod, ABC
import threading

from mock.inst import Locale, HttpServletRequest, HttpServletResponse
from web.context.support.WebApplicationObjectSupport import WebApplicationObjectSupport
from springframework.web.servlet import View
from springframework.web.servlet import ViewResolver


class UnresolvedView(View):
    def get_content_type(self) -> str:
        return None

    def render(self, model: dict, request: HttpServletRequest, response: HttpServletResponse) -> None:
        pass


class AbstractCachingViewResolver(WebApplicationObjectSupport, ViewResolver, ABC):

    # Default maximum number of entries for the view cache: 1024.
	DEFAULT_CACHE_LIMIT = 1024

    lock = threading.Lock()

    _UNRESOLVED_VIEW = UnresolvedView()

    # Default cache filter that always caches.
    # TODO: 
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
    # TODO

    # Specify the maximum number of entries for the view cache.
    # Default is 1024.
    def set_cache_limit(self, cacheLimit: int) -> None:
        self.cacheLimit = cacheLimit

    # Return the maximum number of entries for the view cache.
    def getcache_limit(self) -> int:
        return self.cacheLimit

    # Enable or disable caching.
    # Disable this only for debugging and development.
    def set_cache(self, cache: bool) -> None:
        self.cacheLimit = (DEFAULT_CACHE_LIMIT if cache else 0)

    # Return if caching is enabled.
    def is_cache(self) -> bool:
        return (self.cacheLimit > 0)

    def set_cache_unresolved(self, cacheUnresolved: bool) -> None:
        self.cacheUnresolved = cacheUnresolved

    # Return if caching of unresolved views is enabled.
    def is_cache_unresolved(self) -> bool:
        return self.cacheUnresolved

    def set_cache_filter(self, cacheFilter: CacheFilter) -> None:
        assert cacheFilter is not None
        self.cacheFilter = cacheFilter

    def get_cache_filter(self) -> CacheFilter:
        return self.cacheFilter

    def resolve_view_name(self, viewName: str, locale: Locale) -> View:
        if (not self.is_cache()):
            return self.create_view(viewName, locale)

        else:
            cacheKey = self.get_cache_key(viewName, locale)
            view = self.viewAccessCache.get(cacheKey)
            if (view is None):
                with self.lock:
                    view = self.viewCreationCache.get(cacheKey)
                    if (view is None):
                        # Ask the subclass to create the View object.
                        view = self.create_view(viewName, locale)
                        if (view is None and self.cacheUnresolved):
                            view = self._UNRESOLVED_VIEW
                        
                        if (view != None and self.cacheFilter.filter(viewName, locale)):
                            self.viewAccessCache[cacheKey] = view
                            self.viewCreationCache[cacheKey] = view

            return (view if view != self._UNRESOLVED_VIEW else None)
    
    def _format_key(self, cacheKey: object) -> str:
        return "View with key [" + cacheKey + "] "

    def get_cache_key(self, viewName: str, locale: Locale) -> object:
        return viewName + '_' + locale

    def remove_from_cache(self, viewName: str, locale: Locale) -> None:
        if isCache():
            cacheKey = self.get_cache_key(viewName, locale)
            with self.lock:
                self.viewAccessCache.pop(cacheKey, None)
                cachedView = self.viewCreationCache.pop(cacheKey, None)

    def clear_cache(self) -> None:
        with self.lock:
            self.viewAccessCache = dict()
            self.viewCreationCache = dict()

    def create_view(self, viewName: str, locale: Locale) -> View:
        return self.loadView(viewName, locale)

    @abstractmethod
    def load_view(self, viewName: str, locale: Locale) -> View:
        pass

    class CacheFilter():
        def filter(self, view, viewName, locale):
            pass
            
