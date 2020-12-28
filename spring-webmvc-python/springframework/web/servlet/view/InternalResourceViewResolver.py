from unittest import mock
from springframework.web.servlet import UrlBasedViewResolver
from springframework.utils.mock.type import JstlView
from springframework.web.servlet.view import InternalResourceView, AbstractUrlBasedView


class InternalResourceViewResolver(UrlBasedViewResolver):
    _jstlPresent = True
    # ClassUtils.isPresent("javax.servlet.jsp.jstl.core.Config", InternalResourceViewResolver.class.getClassLoader())

    def __init__(self, prefix: str = None, suffix: str = None):
        viewClass = self.required_view_class()
        if (isinstance(InternalResourceView, viewClass) and self._jstlPresent):
            viewClass = JstlView
        self.set_view_class(viewClass)

        if (prefix is not None) and (suffix is not None):
            self.set_prefix(prefix)
            self.set_suffix(suffix)

    def set_always_include(self, alwaysInclude: bool) -> None:
        self.alwaysInclude = alwaysInclude

    def required_view_class(self):
        return InternalResourceView

    def instantiate_view(self) -> AbstractUrlBasedView:
        if isinstance(self.get_view_class(), InternalResourceView):
            return InternalResourceView()
        elif isinstance(self.get_view_class(), JstlView):
            JstlViewInst = mock.MagicMock(name="JstlView")
            JstlViewInst.__class__ = JstlView
            return JstlViewInst
        else:
            return super().instantiateView()

    def build_view(self, viewName: str) -> AbstractUrlBasedView:
        view = super().build_view(viewName)
        if (self.alwaysInclude is not None):
            view.set_always_include(self.alwaysInclude)

        view.set_prevent_dispatch_loop(True)
        return view
