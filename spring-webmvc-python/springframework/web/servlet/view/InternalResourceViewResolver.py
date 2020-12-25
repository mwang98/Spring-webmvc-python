from springframework.web.servlet import UrlBasedViewResolver
from springframework.utils.mock.inst import ClassUtils, JstlView


class InternalResourceViewResolver(UrlBasedViewResolver):
    _jstlPresent = ClassUtils.isPresent("javax.servlet.jsp.jstl.core.Config", InternalResourceViewResolver.class.getClassLoader())

    def __init__(self):
        viewClase = self.required_view_class()
        if (isinstance(InternalResourceView, viewClass) and self._jstlPresent):
            viewClass = JstlView.__class__

        self.set_view_class(viewClass)

    def set_always_include(self, alwaysInclude: bool) -> None:
        self.alwaysInclude = alwaysInclude

    def required_view_class(self):
        return InternalResourceView.__class__

    def instantiate_view(self) -> AbstractUrlBasedView:
        return (InternalResourceView() if self.get_view_class() == InternalResourceView.__class__ else
                (JstlView() if self.get_view_class() == JstlView.__class__ else super().instantiate_view()))

    def build_view(self, viewName: str) -> AbstractUrlBasedView:
        view = (InternalResourceView) super().build_view(viewName)
        if (self.alwaysInclude != None):
            view.set_always_include(self.alwaysInclude)

        view.set_prevent_dispatch_loop(True)
        return view
