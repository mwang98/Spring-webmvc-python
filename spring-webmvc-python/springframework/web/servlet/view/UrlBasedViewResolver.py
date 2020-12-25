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

    def setViewClass(self, viewClass) -> None:
        if (viewClass != None and not self.requiredViewClass().isAssignableFrom(viewClass)):
            raise Exception("Given view class[" + viewClass.getName() +
					"] is not of type [" + self.requiredViewClass().getName() + "]"))

        self.viewClass = viewClass

    def getViewClass(self) -> object:
        return self.viewClass

    def setPrefix(self, prefix) -> None:
        self.prefix = (prefix if prefix != None else "")

    def getPrefix(self) -> str:
        return self.prefix

    def setSuffix(self, suffix) -> None:
        self.suffix = (suffix if suffix != None else "")

    def getSuffix(self) -> str:
        return self.suffix

    def setContentType(self, contentType) -> None:
        self._contentType = contentType

    def getContentType(self) -> str:
        return self._contentType

    def setRedirectContextRelative(self, redirectContextRelative) -> None:
        self._redirectContextRelative = redirectContextRelative

    def isRedirectContextRelative(self) -> bool:
        return self._redirectContextRelative

    def setRedirectHttp10Compatible(self, redirectHttp10Compatible) -> None:
        self._redirectHttp10Compatible = redirectHttp10Compatible

    def isRedirectHttp10Compatible(self) -> bool:
        return self._redirectHttp10Compatible

    def setRedirectHosts(self, redirectHosts) -> None:
        self._redirectHosts = redirectHosts

    def getRedirectHosts(self) -> list:
        return self._redirectHosts
    
    def setRequestContextAttribute(self, requestContextAttribute) -> None:
        self._requestContextAttribute = requestContextAttribute

    def getRequestContextAttribute(self) -> str:
        return self._requestContextAttribute

    def setAttributesMap(self, attributes) -> None:
        if (attributes != None):
            self._staticAttributes.putAll(attributes)

    def getAttributesMap(self) -> dict:
        return self._staticAttributes

    def setExposePathVariables(self, exposePathVariables) -> None:
        self.exposePathVariables = exposePathVariables

    def getExposePathVariables(self) -> bool:
        return self.exposePathVariables

    def setExposeContextBeansAsAttributes(self, exposeContextBeansAsAttributes) -> None:
        self.exposeContextBeansAsAttributes = exposeContextBeansAsAttributes

    def getExposeContextBeansAsAttributes(self) -> bool:
        return self.exposeContextBeansAsAttributes

    def setExposedContextBeanNames(self, exposedContextBeanNames) -> None:
        self.exposedContextBeanNames = exposedContextBeanNames

    def getExposedContextBeanNames(self) -> list:
        return self.exposedContextBeanNames

    def setViewNames(self, viewNames) -> None:
        self.viewNames = viewNames

    def getViewNames(self) -> list:
        return self.viewNames

    def setOrder(self, order) -> None:
        self.order = order

    def getOrder(self):
        return self.order

    def initApplicationContext(self) -> None:
        super().initApplicationContext()
        if (getViewClass() == None):
            raise Exception("Property 'viewClass' is required")

    def getCacheKey(self, viewName, locale) -> object:
        return viewName

    def createView(self, viewName, locale) -> View:
        if not self.canHandle(viewName, locale):
            return None

        # Check for special "redirect:" prefix.
        if (viewName.startsWith(REDIRECT_URL_PREFIX)):
            redirectUrl = viewName[:len(REDIRECT_URL_PREFIX)]
            view = RedirectView(redirectUrl, 
                    isRedirectContextRelative(), isRedirectHttp10Compatible())
            hosts = getRedirectHosts()
            if (hosts != None):
                view.setHosts(hosts)
            
            return self.applyLifecycleMethods(REDIRECT_URL_PREFIX, view)

        # check for special "forward:" prefix.
        if (viewName.startsWith(FORWARD_URL_PREFIX)):
            forwardUrl = viewName[:len(FORWARD_URL_PREFIX)]
            view = InternalResourceView(forwardUrl)
            return self.applyLifecycleMethods(FORWARD_URL_PREFIX, view)

        # Else fall back to superclass implementation: calling loadView.
        return super().createView(viewName, locale)

    def canHandle(self, viewName, locale) -> bool:
        viewNames = self.getViewNames()
        # todo sptringframework.util.PatternMatchUtils
        return (viewNames == None or PatternMatchUtils.simpleMatch(viewNames, viewName))

    #todo class?
    def requiredViewClass(self) -> class:
        return AbstractUrlBasedView.class

    #todo beans.BeanUtils
    # def instantiateView():
    #     viewClass = getViewClass()
    #     assert viewClass != None
    #     return BeanUtils.instantiateClass(viewClass)

    def loadView(self, viewName, locale) -> View:
        view = self.buildView(viewName)
        result = self.applyLifecycleMethods(viewName, view)
        return (result if view.checkResource(locale) else None)

    def buildView(self, viewName) -> AbstractUrlBasedView:
        view = self.instantiateView()
        view.setUrl(getPrefix() + viewName + getSuffix())
        view.setAttributesMap(getAttributesMap())

        contentType = self.getContentType()
        if (contentType != None):
            view.setContentType(contentType)

        requestContextAttribute = self.getRequestContextAttribute()
        if (requestContextAttribute != None):
            view.setRequestContextAttribute(requestContextAttribute)

        exposePathVariables = self.getExposePathVariables()
        if (exposePathVariables != None):
            view.setExposePathVariables(exposePathVariables)

        exposeContextBeansAsAttributes = self.getExposeContextBeansAsAttributes()
        if (exposeContextBeansAsAttributes != None):
            view.setExposeContextBeansAsAttributes(exposeContextBeansAsAttributes)

        exposedContextBeanNames = self.getExposedContextBeanNames()
        if (exposedContextBeanNames != None):
            view.setExposedContextBeanNames(exposedContextBeanNames)

        return view

    # todo casting / beanfactory
    def applyLifecycleMethods(viewName, view):
    #     context = getApplicationConext()
    #     if (context != None):
    #         initialized = context.getAutowireCapableBeanFactory().initializeBean(view, viewName)
    #         if (initialized instanceof View):
    #             return (View) initialized

        return view

    
