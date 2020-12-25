from abc import abstractmethod, ABC
from springframework.web.servelt import View
#import redirectView

class UrlBasedViewResolver(AbstractCachingViewResolver, Ordered, ABC):
    REDIRECT_URL_PREFIX = "redirect:"
    FORWARD_URL_PREFIX = "forward:"

    # _viewClass
    _prefix = ""
    _suffix = ""
    #_contentType
    _redirectContextRelative = True
    _redirectHttp10Compatible = True
    #_redirectHosts
    #_requestContextAttribute

    _staticAttributes = dict()

    # _order = Ordered.LOWEST_PRECEDENCE todo(core.Ordered)

    def set_view_class(self, viewClass) -> None:
        # isAssignableFrom()? and getName()?
        # if (viewClass != None and not self.required_view_class().isAssignableFrom(viewClass)):
        #     raise Exception("Given view class[" + viewClass.getName() +
		# 			"] is not of type [" + self.required_view_class().getName() + "]"))

        self.viewClass = viewClass

    def get_view_class(self) -> object:
        return self.viewClass

    def set_prefix(self, prefix) -> None:
        self.prefix = (prefix if prefix != None else "")

    def get_prefix(self) -> str:
        return self.prefix

    def set_suffix(self, suffix) -> None:
        self.suffix = (suffix if suffix != None else "")

    def get_suffix(self) -> str:
        return self.suffix

    def set_content_type(self, contentType) -> None:
        self._contentType = contentType

    def get_content_type(self) -> str:
        return self._contentType

    def set_Redirect_context_relative(self, redirectContextRelative) -> None:
        self._redirectContextRelative = redirectContextRelative

    def is_redirect_context_relative(self) -> bool:
        return self._redirectContextRelative

    def set_redirect_http10_compatible(self, redirectHttp10Compatible) -> None:
        self._redirectHttp10Compatible = redirectHttp10Compatible

    def is_redirect_http10_compatible(self) -> bool:
        return self._redirectHttp10Compatible

    def set_redirect_hosts(self, redirectHosts) -> None:
        self._redirectHosts = redirectHosts

    def get_redirect_hosts(self) -> list:
        return self._redirectHosts
    
    def set_request_context_attribute(self, requestContextAttribute) -> None:
        self._requestContextAttribute = requestContextAttribute

    def get_request_context_attribute(self) -> str:
        return self._requestContextAttribute

    def set_attributes_map(self, attributes) -> None:
        if (attributes is not None):
            # TODO: map putAll()
            # self._staticAttributes.putAll(attributes)

    def get_attributes_map(self) -> dict:
        return self._staticAttributes

    def set_Expose_path_variables(self, exposePathVariables) -> None:
        self.exposePathVariables = exposePathVariables

    def get_expose_path_variables(self) -> bool:
        return self.exposePathVariables

    def set_expose_context_beans_as_attributes(self, exposeContextBeansAsAttributes) -> None:
        self.exposeContextBeansAsAttributes = exposeContextBeansAsAttributes

    def get_expose_context_beans_as_attributes(self) -> bool:
        return self.exposeContextBeansAsAttributes

    def set_exposed_context_bean_names(self, exposedContextBeanNames) -> None:
        self.exposedContextBeanNames = exposedContextBeanNames

    def get_exposed_context_bean_names(self) -> list:
        return self.exposedContextBeanNames

    def set_view_names(self, viewNames) -> None:
        self.viewNames = viewNames

    def get_view_names(self) -> list:
        return self.viewNames

    def set_order(self, order) -> None:
        self._order = order

    def get_order(self):
        return self._order

    def init_application_context(self) -> None:
        super().init_application_context()
        if (get_view_class() == None):
            raise Exception("Property 'viewClass' is required")

    def get_cache_key(self, viewName, locale) -> object:
        return viewName

    def create_view(self, viewName, locale) -> View:
        if not self.can_handle(viewName, locale):
            return None

        # Check for special "redirect:" prefix.
        if (viewName.startsWith(REDIRECT_URL_PREFIX)):
            redirectUrl = viewName[:len(REDIRECT_URL_PREFIX)]
            view = RedirectView(redirectUrl, 
                    self.is_redirect_context_relative(), self.is_redirect_http10_compatible())
            hosts = self.get_redirect_hosts()
            if (hosts != None):
                view.set_hosts(hosts)
            
            return self.apply_lifecycle_methods(REDIRECT_URL_PREFIX, view)

        # check for special "forward:" prefix.
        if (viewName.startsWith(FORWARD_URL_PREFIX)):
            forwardUrl = viewName[:len(FORWARD_URL_PREFIX)]
            view = InternalResourceView(forwardUrl)
            return self.apply_lifecycle_methods(FORWARD_URL_PREFIX, view)

        # Else fall back to superclass implementation: calling loadView.
        return super().create_view(viewName, locale)

    def can_handle(self, viewName, locale) -> bool:
        viewNames = self.get_view_names()
        # TODO: sptringframework.util.PatternMatchUtils
        # return (viewNames == None or PatternMatchUtils.simpleMatch(viewNames, viewName))
        return false

    def required_view_class(self) -> class:
        return AbstractUrlBasedView.__class__

    #todo beans.BeanUtils
    # def instantiate_view():
    #     viewClass = get_view_class()
    #     assert viewClass != None
    #     return BeanUtils.instantiateClass(viewClass)

    def load_view(self, viewName, locale) -> View:
        view = self.build_view(viewName)
        result = self.apply_lifecycle_methods(viewName, view)
        return (result if view.check_resource(locale) else None)

    def build_view(self, viewName) -> AbstractUrlBasedView:
        view = self.instantiate_view()
        view.set_url(self.get_prefix() + viewName + self.get_suffix())
        view.set_attributes_map(self.get_attributes_map())

        contentType = self.get_content_type()
        if (contentType != None):
            view.set_content_type(contentType)

        requestContextAttribute = self.get_request_context_attribute()
        if (requestContextAttribute != None):
            view.set_request_context_attribute(requestContextAttribute)

        exposePathVariables = self.get_expose_path_variables()
        if (exposePathVariables != None):
            view.set_expose_path_variables(exposePathVariables)

        exposeContextBeansAsAttributes = self.get_expose_context_beans_as_attributes()
        if (exposeContextBeansAsAttributes != None):
            view.set_expose_context_beans_as_attributes(exposeContextBeansAsAttributes)

        exposedContextBeanNames = self.get_exposed_context_bean_names()
        if (exposedContextBeanNames != None):
            view.set_exposed_context_bean_names(exposedContextBeanNames)

        return view

    # TODO: casting / beanfactory
    def apply_lifecycle_methods(viewName, view):
    #     context = self.get_application_conext()
    #     if (context != None):
    #         initialized = context.get_autowire_capable_bean_factory().initialize_bean(view, viewName)
    #         if (initialized instanceof View):
    #             return (View) initialized

        return view

    
