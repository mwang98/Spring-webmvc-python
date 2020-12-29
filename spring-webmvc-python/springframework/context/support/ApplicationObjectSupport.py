from abc import ABC

from springframework.context.ApplicationContextAware import ApplicationContextAware
from springframework.context.ApplicationContext import ApplicationContext
from springframework.context.support.MessageSourceAccessor import MessageSourceAccessor


class ApplicationObjectSupport(ApplicationContextAware, ABC):
    def __init__(self):
        super().__init__()
        self._application_context: ApplicationContext
        self._message_source_accessor: MessageSourceAccessor

    def set_application_context(self, context: ApplicationContext = None) -> None:
        if context is None and not self.is_context_required():
            self._application_context, self._message_source_accessor = None, None
        elif self._application_context is None:
            if not isinstance(self.required_context_class(), context):
                raise ValueError(
                    "Invalid application context: needs to be of type [" + self.required_context_class().__name__ + "]")
            self._application_context = context
            self._message_source_accessor = MessageSourceAccessor(context)
            self.init_application_context(context)
        else:
            if self._application_context is not context:
                raise ValueError("Cannot reinitialize with different application context: current one is [" +
                                 self._application_context + "], passed-in one is [" + context + "]")

    def is_context_required(self):
        return False

    def required_context_class(self):
        return ApplicationContext.__class__

    def init_application_context(self, context: ApplicationContext = None) -> None:
        if context is not None:
            self.init_application_context()

    def get_application_context(self):
        if self._application_context is None and self.is_context_required():
            raise ValueError(
                "ApplicationObjectSupport instance [" + str(self) + "] does not run in an ApplicationContext")
        return self._application_context

    def obtain_application_context(self):
        application_context = self.get_application_context()
        if application_context is None:
            raise ValueError("No ApplicationContext")
        return application_context

    def get_message_source_accessor(self):
        if self._message_source_accessor is None and self.is_context_required():
            raise ValueError(
                "ApplicationObjectSupport instance [" + str(self) + "] does not run in an ApplicationContext")
        return self._message_source_accessor
