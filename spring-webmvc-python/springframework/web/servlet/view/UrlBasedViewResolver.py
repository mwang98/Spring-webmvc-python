from abc import ABC
from springframework.web.servlet import View
from springframework.web.servlet import RedirectView
from springframework.utils.mock.inst import Ordered, BeanUtils
from .InternalResourceView import InternalResourceView
from .AbstractCachingViewResolver import AbstractCachingViewResolver
from .AbstractUrlBasedView import AbstractUrlBasedView


class UrlBasedViewResolver(AbstractCachingViewResolver, Ordered, ABC):
    REDIRECT_URL_PREFIX = "redirect:"
    FORWARD_URL_PREFIX = "forward:"
    _prefix = ""
    _suffix = ""
    _redirectContextRelative = True
    _redirectHttp10Compatible = True
    _staticAttributes = dict()
    _order = Ordered.LOWEST_PRECEDENCE

    def set_view_class(self, viewClass) -> None:
        # TODO: isAssignableFrom()? and getName()?
        if viewClass is not None and \
                not issubclass(self.required_view_class(), viewClass):
            raise Exception(f"Given view class[{viewClass.getName()}] is not of \
                type [{self.required_view_class().getName()}]")

        self.viewClass = viewClass

    def get_view_class(self):
        return self.viewClass

    def set_prefix(self, prefix: str) -> None:
        self.prefix = (prefix if prefix is not None else "")

    def get_prefix(self) -> str:
        return self.prefix

    def set_suffix(self, suffix: str) -> None:
        self.suffix = (suffix if suffix != None else "")

    def get_suffix(self) -> str:
        return self.suffix

    def set_content_type(self, contentType: str) -> None:
        self._contentType = contentType

    def get_content_type(self) -> str:
        return self._contentType

    def set_Redirect_context_relative(self, redirectContextRelative: bool) -> None:
        self._redirectContextRelative = redirectContextRelative

    def is_redirect_context_relative(self) -> bool:
        return self._redirectContextRelative

    def set_redirect_http10_compatible(self, redirectHttp10Compatible: bool) -> None:
        self._redirectHttp10Compatible = redirectHttp10Compatible

    def is_redirect_http10_compatible(self) -> bool:
        return self._redirectHttp10Compatible

    def set_redirect_hosts(self, redirectHosts: list) -> None:
        self._redirectHosts = redirectHosts

    def get_redirect_hosts(self) -> list:
        return self._redirectHosts

    def set_request_context_attribute(self, requestContextAttribute: str) -> None:
        self._requestContextAttribute = requestContextAttribute

    def get_request_context_attribute(self) -> str:
        return self._requestContextAttribute

    def set_attributes(self, props) -> None:
        self._staticAttributes.update(props)

    def set_attributes_map(self, attributes: dict) -> None:
        if (attributes is not None):
            self._staticAttributes.update(attributes)

    def get_attributes_map(self) -> dict:
        return self._staticAttributes

    def set_expose_path_variables(self, exposePathVariables: bool) -> None:
        self.exposePathVariables = exposePathVariables

    def get_expose_path_variables(self) -> bool:
        return self.exposePathVariables

    def set_expose_context_beans_as_attributes(self, exposeContextBeansAsAttributes: bool) -> None:
        self.exposeContextBeansAsAttributes = exposeContextBeansAsAttributes

    def get_expose_context_beans_as_attributes(self) -> bool:
        return self.exposeContextBeansAsAttributes

    def set_exposed_context_bean_names(self, exposedContextBeanNames: list) -> None:
        self.exposedContextBeanNames = exposedContextBeanNames

    def get_exposed_context_bean_names(self) -> list:
        return self.exposedContextBeanNames

    def set_view_names(self, viewNames: list) -> None:
        self.viewNames = viewNames

    def get_view_names(self) -> list:
        return self.viewNames

    def set_order(self, order) -> None:
        self._order = order

    def get_order(self):
        return self._order

    def init_application_context(self) -> None:
        super().init_application_context()
        if (self.get_view_class() is None):
            raise Exception("Property 'viewClass' is required")

    def get_cache_key(self, viewName: str, locale) -> object:
        return viewName

    def create_view(self, viewName: str, locale) -> View:
        if not self.can_handle(viewName, locale):
            return None

        # Check for special "redirect:" prefix.
        if (viewName.startsWith(self.REDIRECT_URL_PREFIX)):
            redirectUrl = viewName[:len(self.REDIRECT_URL_PREFIX)]
            view = RedirectView(redirectUrl,
                                self.is_redirect_context_relative(), self.is_redirect_http10_compatible())
            hosts = self.get_redirect_hosts()
            if (hosts is not None):
                view.set_hosts(hosts)

            return self.apply_lifecycle_methods(self.REDIRECT_URL_PREFIX, view)

        # check for special "forward:" prefix.
        if (viewName.startsWith(self.FORWARD_URL_PREFIX)):
            forwardUrl = viewName[:len(self.FORWARD_URL_PREFIX)]
            view = InternalResourceView(forwardUrl)
            return self.apply_lifecycle_methods(self.FORWARD_URL_PREFIX, view)

        # Else fall back to superclass implementation: calling loadView.
        return super().create_view(viewName, locale)

    def can_handle(self, viewName: str, locale) -> bool:
        viewNames = self.get_view_names()
        return (viewNames is None or any([(viewName in pattern) for pattern in viewNames]))
        # PatternMatchUtils.simpleMatch(viewNames, viewName))

    def required_view_class(self):
        return AbstractUrlBasedView

    def instantiate_view(self):
        viewClass = self.get_view_class()
        assert viewClass is not None
        return BeanUtils.instantiateClass(viewClass)

    def load_view(self, viewName: str, locale) -> View:
        view = self.build_view(viewName)
        result = self.apply_lifecycle_methods(viewName, view)
        return (result if view.check_resource(locale) else None)

    def build_view(self, viewName: str) -> AbstractUrlBasedView:
        view = self.instantiate_view()
        view.set_url(self.get_prefix() + viewName + self.get_suffix())
        view.set_attributes_map(self.get_attributes_map())

        contentType = self.get_content_type()
        if (contentType is not None):
            view.set_content_type(contentType)

        requestContextAttribute = self.get_request_context_attribute()
        if (requestContextAttribute is not None):
            view.set_request_context_attribute(requestContextAttribute)

        exposePathVariables = self.get_expose_path_variables()
        if (exposePathVariables is not None):
            view.set_expose_path_variables(exposePathVariables)

        exposeContextBeansAsAttributes = self.get_expose_context_beans_as_attributes()
        if (exposeContextBeansAsAttributes is not None):
            view.set_expose_context_beans_as_attributes(
                exposeContextBeansAsAttributes)

        exposedContextBeanNames = self.get_exposed_context_bean_names()
        if (exposedContextBeanNames is not None):
            view.set_exposed_context_bean_names(exposedContextBeanNames)

        return view

    def apply_lifecycle_methods(self, viewName: str, view: AbstractUrlBasedView) -> View:
        # TODO: getApplicationContext
        context = self.get_application_onext()
        if (context is not None):
            initialized = context.get_autowire_capable_bean_factory().initialize_bean(view, viewName)
            if isinstance(initialized, View):
                return initialized

        return view
