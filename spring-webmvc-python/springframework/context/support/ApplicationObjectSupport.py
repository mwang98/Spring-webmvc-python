from abc import ABC

import ApplicationContextAware
import ApplicationContext

class ApplicationObjectSupport(ApplicationContextAware, ABC):
    def __init__(self):
        _application_context: ApplicationContext = None
        _message_source_accessor: MessageSourceAccessor = None

