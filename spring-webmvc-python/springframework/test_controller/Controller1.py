from springframework.web.servlet.ModelAndView import ModelAndView
from springframework.web.servlet.mvc.Controller import Controller
from springframework.utils.mock.inst import HttpServletResponse, HttpServletRequest
from springframework.web.servlet.view import InternalResourceView
from springframework.web.testfixture.servlet import MockHttpServletRequest, MockHttpServletResponse


class Controller1(Controller):
    def handle_request(self, request: MockHttpServletRequest, response: MockHttpServletResponse):
        print("Controller1 invoked!!!")
        mav = ModelAndView()
        print(request.get_request_url())
        internalResourceView = InternalResourceView(request.get_request_url())
        mav.set_view(internalResourceView)
        return mav