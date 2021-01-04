from springframework.web.servlet.ModelAndView import ModelAndView
from springframework.web.servlet.mvc.Controller import Controller
from springframework.utils.mock.inst import HttpServletResponse, HttpServletRequest


class Controller1(Controller):
    def handle_request(self, request: HttpServletRequest, response: HttpServletResponse):
        print("Controller1 invoked!!!")
        mav = ModelAndView()
        return mav