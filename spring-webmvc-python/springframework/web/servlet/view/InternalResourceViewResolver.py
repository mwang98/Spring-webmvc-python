from springframework.web.servlet import UrlBasedViewResolver
#classUtils

class InternalResourceViewResolver(UrlBasedViewResolver):
    # _jstlPresent = ClassUtils.isPresent("javax.servlet.jsp.jstl.core.Config", InternalResourceViewResolver.class.getClassLoader())

    # (bool)alwaysInclude

    #todo
    def __init__(self):
        viewClase = self.requiredViewClass()
        if (InternalResourceView.class == viewClass and jstlPresent):
            viewClass = JstlView.class

        self.setViewClass(viewClass)

    def setAlwaysInclude(self, alwaysInclude: bool) -> None:
        self.alwaysInclude = alwaysInclude

    def requiredViewClass(self) -> class:
        return InternalResourceView.class

    def instantiateView(self) -> AbstractUrlBasedView:
        return (InternalResourceVIew() if self.getViewClass() == InternalResourceView.class else
            (JstlView() if self.getViewClass() == JstlView.class else super.instantiateView()))

    def buildView(self, viewName: str) -> AbstractUrlBasedView:
        view = (InternalResourceView) super().buildView(viewName)
        if (self.alwaysInclude != None):
            view.setAlwaysInclude(self.alwaysInclude)

        view.setPreventDispatchLoop(True)
        return view
