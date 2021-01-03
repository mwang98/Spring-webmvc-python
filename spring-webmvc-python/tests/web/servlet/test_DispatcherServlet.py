
from springframework.web.servlet.DispatcherServlet import DispatcherServlet
from springframework.web.testfixture.servlet.MockServletConfig import MockServletConfig
from springframework.web.testfixture.servlet.MockServletContext import MockServletContext
from springframework.web.testfixture.servlet.MockHttpServletRequest import MockHttpServletRequest
from springframework.web.testfixture.servlet.MockHttpServletResponse import MockHttpServletResponse

def main():
    print('strat')
    servletConfig = MockServletConfig(MockServletContext, servletName='simple')
    dispatcherServelet = DispatcherServlet()
    dispatcherServelet.init(servletConfig)

    request = MockHttpServletRequest(servletConfig.get_servlet_context(), "GET", "/locale.do")
    #request.addPreferredLocale(Locale.CANADA)
    response = MockHttpServletResponse()

    #dispatcherServelet.set_context_class()
    dispatcherServelet.do_service(request, response)
    print('test finished')


if __name__ == '__main__':
    main()
