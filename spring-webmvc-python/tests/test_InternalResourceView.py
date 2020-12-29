import pytest
from unittest import TestCase
from springframework.web.testfixture.servlet import MockHttpServletRequest as HttpServletRequest
from InternalResourceView import InternalResourceView


@pytest.mark.skip("half way to complete")
class TestInternalResourceView(TestCase):
    _model = {'foo': 'bar', 'I': 1}
    url = 'forward-to'

    def setUp(self) -> None:
        self.request = HttpServletRequest()
        self.view = InternalResourceView()

    def test_set_always_include(self):
        with self.assertRaises(ValueError):
            self.view.after_properties_set()
        # self.fail()

    def test_render_merged_output_model(self):
        self.skipTest("TODO")
        # self.fail()

    def test_use_include(self):
        self.skipTest("TODO")
        # self.fail()
