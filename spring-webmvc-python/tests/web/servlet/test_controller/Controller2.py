from springframework.web.servlet.mvc.Controller import Controller
from springframework.utils.mock.inst import HttpServletResponse, HttpServletRequest
from springframework.web.servlet import ModelAndView

class Controller2(Controller):
    def handle_request(self, request: HttpServletRequest, response: HttpServletResponse):
        print("Controller2 invoked!!!")
        mav = ModelAndView()
        return mav