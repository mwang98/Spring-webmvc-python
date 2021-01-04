from springframework.web.servlet.ModelAndView import ModelAndView
from springframework.web.servlet.mvc.Controller import Controller
from springframework.utils.mock.inst import HttpServletResponse, HttpServletRequest
from springframework.web.servlet.view import InternalResourceView


class Controller1(Controller):
    def handle_request(self, request: HttpServletRequest, response: HttpServletResponse):
        print("Controller1 invoked!!!")
        mav = ModelAndView()
        internalResourceView = InternalResourceView()
        print('inview:',internalResourceView)
        mav.set_view(internalResourceView)
        return mav