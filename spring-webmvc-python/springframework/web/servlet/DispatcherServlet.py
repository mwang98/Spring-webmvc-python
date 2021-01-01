class DispatcherServlet(object):
    """docstring for DispatcherServlet"""
    contextClass = None
    config = None
    webApplicationContext = None

    def __init__(self):
        super(DispatcherServlet, self).__init__()
        #self.arg = arg

    def init(self, config):
        self.config = config

        '''
        PropertyValues   pvs = new
        ServletConfigPropertyValues(getServletConfig(), this.requiredProperties);
        if (!pvs.isEmpty()) {
        try {
        BeanWrapper bw = PropertyAccessorFactory.forBeanPropertyAccess(this);
        ResourceLoader resourceLoader = new ServletContextResourceLoader(getServletContext());
        bw.registerCustomEditor(Resource.

        class , new ResourceEditor(resourceLoader, getEnvironment()));
        initBeanWrapper(bw);
        bw.setPropertyValues(pvs, true);
        }
        catch (BeansException ex) {
        if (logger.isErrorEnabled()) {

        logger.error("Failed to set bean properties on servlet '" + getServletName() + "'", ex);
        '''
        self.init_servlet_bean()

    def init_servlet_bean(self):
        '''
        getServletContext().log("Initializing Spring " + getClass().getSimpleName() + " '" + getServletName() + "'");
        if (logger.isInfoEnabled()) {
        logger.info("Initializing Servlet '" + getServletName() + "'");
        }
        long
        startTime = System.currentTimeMillis();
        '''

        self.webApplicationContext = self.init_web_application_context()

    def init_web_application_context(self):
        context=None
        self.on_refresh()
        return 1

    def on_refresh(self, context):
        self.init_strategies(context)

    def init_strategies(self, context):
        raise NotImplementedError

    def set_context_class(self, contextClass):
        self.contextClass = contextClass

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
