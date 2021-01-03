from unittest import TestCase, mock
from springframework.web.testfixture.servlet import MockServletContext
from springframework.web.testfixture.servlet import MockHttpServletRequest
from springframework.web.testfixture.servlet import MockHttpServletResponse
from springframework.web.context.support.StaticWebApplicationContext import StaticWebApplicationContext
from springframework.web.servlet.view import UrlBasedViewResolver, \
    InternalResourceViewResolver, InternalResourceView, JstlView


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

    def test_internal_resourceV_view_resolver_without_prefixes(self):
        self.do_test_url_based_view_resolver_without_prefixes(InternalResourceViewResolver())

    def test_internal_resourceV_view_resolver_with_prefixes(self):
        self.do_test_url_based_view_resolver_with_prefixes(InternalResourceViewResolver())

    def do_test_url_based_view_resolver_without_prefixes(self, vr):
        pass

    def do_test_url_based_view_resolver_with_prefixes(self, vr):
        pass


class testView(InternalResourceView):
    def __init__(self):
        super().__init__(self)
        self.set_request_context_attribute("testRequestContext")

    def set_location(self, location):
        ServletContextResource = mock.MagicMock(name="ServletContextResource")
        if not isinstance(location, ServletContextResource):
            raise Exception(f"Expecting ServletContextResource, not {location.__class__.__name__}")
