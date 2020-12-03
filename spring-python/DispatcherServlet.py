from ServletRequest import SimpleHttpServletRequest


class DispatcherServlet(object):
    def __init__(self):
        pass

    def get_servlet_context(self):
        return servletConfig.getServletContext()

    def locale_request(self):
        request = SimpleHttpServletRequest
