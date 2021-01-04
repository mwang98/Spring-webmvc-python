from springframework.web.servlet.DispatcherServlet import DispatcherServlet
from springframework.web.testfixture.servlet.MockServletConfig import MockServletConfig
from springframework.web.testfixture.servlet.MockServletContext import MockServletContext
from springframework.web.testfixture.servlet.MockHttpServletRequest import MockHttpServletRequest
from springframework.web.testfixture.servlet.MockHttpServletResponse import MockHttpServletResponse

def main():
    print('start')
    servletConfig = MockServletConfig(MockServletContext, servletName='simple')
    dispatcherServelet = DispatcherServlet("../../../../spring-webmvc-demo/HelloSpring/web/WEB-INF/mvc-servlet.xml")
    dispatcherServelet.init(servletConfig)

    request = MockHttpServletRequest(servletConfig.get_servlet_context(), "GET", "/locale.do")
    #request.addPreferredLocale(Locale.CANADA)
    response = MockHttpServletResponse()

    request.set_context_path("/mycontext")
    request.set_servlet_path("/myservlet")
    request.set_path_info(";mypathinfo")
    request.set_query_string("?param1=value1")

    #dispatcherServelet.set_context_class()
    dispatcherServelet.do_service(request, response)
    print('test finished')


if __name__ == '__main__':
    main()
