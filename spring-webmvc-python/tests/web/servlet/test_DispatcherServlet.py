
from springframework.web.servlet.DispatcherServlet import DispatcherServlet
from springframework.web.testfixture.servlet.MockServletConfig import MockServletConfig
from springframework.web.testfixture.servlet.MockServletContext import MockServletContext


def main():
    print('strat')
    servletConfig = MockServletConfig(MockServletContext, servletName='simple')
    dispatcherServelet = DispatcherServlet()

    #dispatcherServelet.set_context_class()
    dispatcherServelet.init(servletConfig)
    print('test finished')


if __name__ == '__main__':
    main()
