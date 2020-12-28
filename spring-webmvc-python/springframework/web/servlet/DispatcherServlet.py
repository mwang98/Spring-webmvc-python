class DispatcherServlet(object):
    """docstring for DispatcherServlet"""

    def __init__(self, arg):
        super(DispatcherServlet, self).__init__()
        self.arg = arg

    def do_service(self, request, response):
        self.do_dispatch(request, response)

    def do_dispatch(self, request, response):
        mapped_handler = self.get_handler(request)
        handler_adapter = self.get_handler_adapter(mapped_handler.getHandler())

        if not mapped_handler.applyPreHandle(request, response):
            return

        model_and_view = handler_adapter.handle(request, response, mapped_handler.getHandler())
        mapped_handler.applyPostHandle(request, response, model_and_view)

        view = model_and_view.getView()
        view.render(model_and_view.getModelInternal(), request, response)

    def get_handler(self, request):
        for handlerMapping in self.handlerMappings:
            handler_execution_chain = handlerMapping.getHandler(request)
            if handler_execution_chain is not None:
                return handler_execution_chain
        return None

    def get_handler_adapter(self, handler):
        for handlerAdapter in self.handlerAdapters:
            if handlerAdapter.supports(handler):
                return handlerAdapter
        return None
