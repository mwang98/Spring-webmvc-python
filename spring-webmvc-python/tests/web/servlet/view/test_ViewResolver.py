import pytest
from unittest import TestCase, mock
from springframework.utils.mock.inst import Locale
from springframework.web.testfixture.servlet import MockServletContext
from springframework.web.testfixture.servlet import MockHttpServletRequest
from springframework.web.testfixture.servlet import MockHttpServletResponse
from springframework.web.context.support.StaticWebApplicationContext import StaticWebApplicationContext
from springframework.web.servlet.DispatcherServlet import DispatcherServlet
from springframework.web.servlet.view import UrlBasedViewResolver, \
    InternalResourceViewResolver, InternalResourceView, JstlView, RedirectView


class TestViewResolver(TestCase):

    def setUp(self):
        self.wac = StaticWebApplicationContext()
        self.sc = MockServletContext()
        self.request = MockHttpServletRequest()
        self.response = MockHttpServletResponse()
        self.wac.set_servlet_context(self.sc)

    def test_url_based_view_resolver_without_prefixes(self):
        vr = UrlBasedViewResolver()
        vr.set_view_class(JstlView)
        self.do_test_url_based_view_resolver_without_prefixes(vr)

    def test_url_based_view_resolver_with_prefixes(self):
        vr = UrlBasedViewResolver()
        vr.set_view_class(JstlView)
        self.do_test_url_based_view_resolver_with_prefixes(vr)

    def test_internal_resource_view_resolver_without_prefixes(self):
        self.do_test_url_based_view_resolver_without_prefixes(InternalResourceViewResolver())

    def test_internal_resource_view_resolver_with_prefixes(self):
        self.do_test_url_based_view_resolver_with_prefixes(InternalResourceViewResolver())

    def do_test_url_based_view_resolver_without_prefixes(self, vr: UrlBasedViewResolver):
        return
        self.wac.refresh()
        vr.set_application_context(self.wac)
        vr.set_content_type("myContentType")
        vr.set_request_context_attribute("rc")

        view = vr.resolve_view_name("example1", Locale.getDefault())
        assert isinstance(view, JstlView), "Incorrect view class"
        assert view.get_url() == "example1", "Incorrect URL"
        assert view.get_content_type() == "myContentType", "Incorrect textContentType"

        view = vr.resolve_view_name("example2", Locale.getDefault())
        assert isinstance(view, JstlView), "Incorrect view class"
        assert view.get_url() == "example2", "Incorrect URL"
        assert view.get_content_type() == "myContentType", "Incorrect textContentType"

        # TODO: self.request.set_attribute

        view = vr.resolve_view_name("redirect:myUrl", Locale.getDefault())
        assert isinstance(view, RedirectView), "Incorrect view class"
        assert view.get_url() == "myUrl", "Incorrect URL"
        #TODO: check applicationContext

        view = vr.resolveViewName("forward:myUrl", Locale.getDefault())
        assert isinstance(view, InternalResourceView), "Incorrect view class"
        assert view.get_url() == "myUrl", "Incorrect URL"

    def do_test_url_based_view_resolver_with_prefixes(self, vr):
        return
        self.wac.refresh()
        vr.set_prefix("/WEB-INF/")
        vr.set_suffix(".jsp")
        vr.set_application_context(self.wac)

        view = vr.resolveViewName("example1", Locale.getDefault())
        assert isinstance(view, JstlView)
        assert view.get_url() == "/WEB_INF/example1.jsp", "Incorrect URL"

        view = vr.resolveViewName("example2", Locale.getDefault())
        assert isinstance(view, JstlView)
        assert view.get_url() == "/WEB_INF/example2.jsp", "Incorrect URL"

        view = vr.resolveViewName("redirect:myUrl", Locale.getDefault())
        assert isinstance(view, RedirectView), "Incorrect view class"
        assert view.get_url() == "myUrl", "Incorrect URL"

        view = vr.resolveViewName("forward:myUrl", Locale.getDefault())
        assert isinstance(view, InternalResourceView), "Incorrect view class"
        assert view.get_url() == "myUrl", "Incorrect URL"


class testView(InternalResourceView):
    def __init__(self):
        super().__init__(self)
        self.set_request_context_attribute("testRequestContext")

    def set_location(self, location):
        ServletContextResource = mock.MagicMock(name="ServletContextResource")
        if not isinstance(location, ServletContextResource):
            raise Exception(f"Expecting ServletContextResource, not {location.__class__.__name__}")
