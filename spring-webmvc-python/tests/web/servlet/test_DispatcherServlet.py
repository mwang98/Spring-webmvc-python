from springframework.web.servlet.DispatcherServlet import DispatcherServlet
from springframework.web.testfixture.servlet.MockServletConfig import MockServletConfig
from springframework.web.testfixture.servlet.MockServletContext import MockServletContext
from springframework.web.testfixture.servlet.MockHttpServletRequest import MockHttpServletRequest
from springframework.web.testfixture.servlet.MockHttpServletResponse import MockHttpServletResponse


def test_1(servletConfig, dispatcherServlet):
    request = MockHttpServletRequest(servletConfig.get_servlet_context(), "GET", "/mycontext/myservlet/hello")
    response = MockHttpServletResponse()

    request.set_context_path("/mycontext")
    request.set_servlet_path("/myservlet")
    request.set_path_info("/hello")
    request.set_query_string("?param1=value1")
    request.set_parameter('team id', [4])
    request.set_parameter('team member num', [6])

    dispatcherServlet.do_service(request, response)
    print('test 1 finished')

def test_2(servletConfig, dispatcherServlet):
    request = MockHttpServletRequest(servletConfig.get_servlet_context(), "GET", "/mycontext/myservlet/welcome")
    response = MockHttpServletResponse()

    request.set_context_path("/mycontext")
    request.set_servlet_path("/myservlet")
    request.set_path_info("/hello")
    request.set_query_string("?param1=value1")
    request.set_parameter('term project', 'spring webmvc')

    dispatcherServlet.do_service(request, response)
    print('test 2 finished')


def main():
    print('start')

    servletConfig = MockServletConfig(MockServletContext, servletName='simple')
    dispatcherServlet = DispatcherServlet('./myservlet.xml')
    dispatcherServlet.init(servletConfig)
    test_2(servletConfig, dispatcherServlet)




if __name__ == '__main__':
    main()
