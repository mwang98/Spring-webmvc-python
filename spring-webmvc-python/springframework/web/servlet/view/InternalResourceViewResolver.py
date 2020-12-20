from springframework.web.servlet import UrlBasedViewResolver
#classUtils

class InternalResourceViewResolver(UrlBasedViewResolver):
    # _jstlPresent = ClassUtils.isPresent("javax.servlet.jsp.jstl.core.Config", InternalResourceViewResolver.class.getClassLoader())

    # (bool)alwaysInclude

    #todo
    __init__(self):
        viewClase = requiredViewClass()
        if (InternalResourceView.class == viewClass and jstlPresent):
            viewClass = JstlView.class

        setViewClass(viewClass)

    def setAlwaysInclude(alwaysInclude: bool) -> None:
        self.alwaysInclude = alwaysInclude

    def requiredViewClass() -> class:
        return InternalResourceView.class

    def instantiateView() -> AbstractUrlBasedView:
        return (InternalResourceVIew() if getViewClass() == InternalResourceView.class else
            (JstlView() if getViewClass() == JstlView.class else super.instantiateView()))

    def buildView(viewName: str) -> AbstractUrlBasedView:
        view = (InternalResourceView) super.buildView(viewName)
        if (this.alwaysInclude != None):
            view.setAlwaysInclude(self.alwaysInclude)

        view.setPreventDispatchLoop(True)
        return view
