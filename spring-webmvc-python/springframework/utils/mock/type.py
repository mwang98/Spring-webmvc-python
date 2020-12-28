from unittest import mock

HttpSessionBindingListener = type("HttpSessionBindingListener", (mock.MagicMock,), {})
Serializable = type("Serializable", (mock.MagicMock,), {})
HttpServletResponseWrapper = type("HttpServletResponseWrapper", (mock.MagicMock,), {})
JstlView = type("JstlView", (mock.MagicMock,), {})
ServletRequestWrapper = type("ServletRequestWrapper", (mock.MagicMock,), {})
