from abc import abstractmethod, ABC
from springframework.web.servelt import View

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

    def setViewClass(viewClass) -> None:
        if (viewClass != None and not requiredViewClass().isAssignableFrom(viewClass)):
            raise Exception("Given view class[" + viewClass.getName() +
					"] is not of type [" + requiredViewClass().getName() + "]"))

        self.viewClass = viewClass

    def getViewClass() -> object:
        return self.viewClass

    def setPrefix(prefix) -> None:
        self.prefix = (prefix if prefix != None else "")

    def getPrefix() -> str:
        return self.prefix

    def setSuffix(suffix) -> None:
        self.suffix = (suffix if suffix != None else "")

    def getSuffix() -> str:
        return self.suffix

    def setContentType(contentType) -> None:
        self._contentType = contentType

    def getContentType() -> str:
        return self._contentType

    def setRedirectContextRelative(redirectContextRelative) -> None:
        self._redirectContextRelative = redirectContextRelative

    def isRedirectContextRelative() -> bool:
        return self._redirectContextRelative

    def setRedirectHttp10Compatible(redirectHttp10Compatible) -> None:
        self._redirectHttp10Compatible = redirectHttp10Compatible

    def isRedirectHttp10Compatible() -> bool:
        return self._redirectHttp10Compatible

    def setRedirectHosts(redirectHosts) -> None:
        self._redirectHosts = redirectHosts

    def getRedirectHosts() -> list:
        return self._redirectHosts
    
    def setRequestContextAttribute(requestContextAttribute) -> None:
        self._requestContextAttribute = requestContextAttribute

    def getRequestContextAttribute() -> str:
        return self._requestContextAttribute

    def setAttributesMap(attributes) -> None:
        if (attributes != None):
            self._staticAttributes.putAll(attributes)

    def getAttributesMap() -> dict:
        return self._staticAttributes

    def setExposePathVariables(exposePathVariables) -> None:
        self.exposePathVariables = exposePathVariables

    def getExposePathVariables() -> bool:
        return self.exposePathVariables

    def setExposeContextBeansAsAttributes(exposeContextBeansAsAttributes) -> None:
        self.exposeContextBeansAsAttributes = exposeContextBeansAsAttributes

    def getExposeContextBeansAsAttributes() -> bool:
        return self.exposeContextBeansAsAttributes

    def setExposedContextBeanNames(exposedContextBeanNames) -> None:
        self.exposedContextBeanNames = exposedContextBeanNames

    def getExposedContextBeanNames() -> list:
        return self.exposedContextBeanNames

    def setViewNames(viewNames) -> None:
        self.viewNames = viewNames

    def getViewNames() -> list:
        return self.viewNames

    def setOrder(order) -> None:
        self.order = order

    def getOrder():
        return self.order

    def initApplicationContext() -> None:
        super().initApplicationContext()
        if (getViewClass() == None):
            raise Exception("Property 'viewClass' is required")

    def getCacheKey(viewName, locale) -> object:
        return viewName

    def createView(viewName, locale) -> View:
        if not canHandle(viewName, locale):
            return None

        # Check for special "redirect:" prefix.
        if (viewName.startsWith(REDIRECT_URL_PREFIX)):
            redirectUrl = viewName[:len(REDIRECT_URL_PREFIX)]
            view = RedirectView(redirectUrl, 
                    isRedirectContextRelative(), isRedirectHttp10Compatible())
            hosts = getRedirectHosts()
            if (hosts != None):
                view.setHosts(hosts)
            
            return applyLifecycleMethods(REDIRECT_URL_PREFIX, view)

        # check for special "forward:" prefix.
        if (viewName.startsWith(FORWARD_URL_PREFIX)):
            forwardUrl = viewName[:len(FORWARD_URL_PREFIX)]
            view = InternalResourceView(forwardUrl)
            return applyLifecycleMethods(FORWARD_URL_PREFIX, view)

        # Else fall back to superclass implementation: calling loadView.
        return super().createView(viewName, locale)

    def canHandle(viewName, locale) -> bool:
        viewNames = getViewNames()
        # todo sptringframework.util.PatternMatchUtils
        return (viewNames == None or PatternMatchUtils.simpleMatch(viewNames, viewName))

    #todo class?
    # def requiredViewClass():
    #     return AbstractUrlBasedView.class

    #todo beans.BeanUtils
    # def instantiateView():
    #     viewClass = getViewClass()
    #     assert viewClass != None
    #     return BeanUtils.instantiateClass(viewClass)

    def loadView(viewName, locale) -> View:
        view = buildView(viewName)
        result = applyLifecycleMethods(viewName, view)
        return (result if view.checkResource(locale) else None)

    def buildView(viewName) -> AbstractUrlBasedView:
        view = instantiateView()
        view.setUrl(getPrefix() + viewName + getSuffix())
        view.setAttributesMap(getAttributesMap())

        contentType = getContentType()
        if (contentType != None):
            view.setContentType(contentType)

        requestContextAttribute = getRequestContextAttribute()
        if (requestContextAttribute != None):
            view.setRequestContextAttribute(requestContextAttribute)

        exposePathVariables = getExposePathVariables()
        if (exposePathVariables != None):
            view.setExposePathVariables(exposePathVariables)

        exposeContextBeansAsAttributes = getExposeContextBeansAsAttributes()
        if (exposeContextBeansAsAttributes != None):
            view.setExposeContextBeansAsAttributes(exposeContextBeansAsAttributes)

        exposedContextBeanNames = getExposedContextBeanNames()
        if (exposedContextBeanNames != None):
            view.setExposedContextBeanNames(exposedContextBeanNames)

        return view

    # todo casting / beanfactory
    # def applyLifecycleMethods(viewName, view):
    #     context = getApplicationConext()
    #     if (context != None):
    #         initialized = context.getAutowireCapableBeanFactory().initializeBean(view, viewName)
    #         if (initialized instanceof View):
    #             return (View) initialized

    #     return view

    
