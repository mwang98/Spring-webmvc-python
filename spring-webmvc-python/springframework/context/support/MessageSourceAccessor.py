


class MessageSourceAccessor():
    def __init__(self, message_source: MessageSource, default_locale: Locale = None):
        self._message_source: MessageSource = message_source
        self._default_locale: Locale = default_locale

    def get_default_locale(self) -> Locale:
        return self._default_locale if self._default_locale is not None else LocaleContextHolder.get_locale()

    def get_message(self, code: str, default_message: str) -> str:
        msg = self._message_source.get_message(code, None, default_message, self.get_default_locale())
        return msg if msg is not None else ''

    # TODO: solve the function overloading issue
    # def get_message(self, code: str, args: list[object], default_message: str) -> str:
