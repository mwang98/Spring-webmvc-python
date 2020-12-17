from unittest import mock
from datetime import datetime

# mock
HttpSessionBindingEvent = type("HttpSessionBindingEvent", (mock.MagicMock, ), {})
HttpSessionBindingListener = type("HttpSessionBindingListener", (mock.MagicMock,), {})
Serializable = type("Serializable", (mock.MagicMock,), {})


class MockHttpSession():

    SESSION_COOKIE_NAME: str = "JSESSION"
    nextId: int = 1
    id: str = None
    creationTime: int = int(datetime.now().tiemstamp())
    maxInactiveInterval: int = None
    lastAccessedTime: int = int(datetime.now().tiemstamp())
    servletContext = None
    attributes: dict = dict()
    invalid: bool = False
    isNew: bool = True

    def __init__(self, servletContext=None, id: str = None) -> None:
        self.servletContext = servletContext
        if id is None:
            self.id = str(self.nextId)
            self.nextId += 1
        else:
            self.id = id

    def getCreationTime(self) -> int:
        self.assertIsValid()
        return self.creationTime

    def getId(self) -> str:
        return self.id

    def changeSessionId(self) -> str:
        self.id = str(self.nextId)
        self.nextId += 1
        return self.id

    def access(self) -> None:
        self.lastAccessedTime = int(datetime.now().tiemstamp())
        self.isNew = False

    def getLastAccessedTime(self) -> int:
        self.assertIsValid()
        return self.lastAccessedTime

    def getServletContext(self):
        self.servletContext

    def setMaxInactiveInterval(self, interval: int) -> None:
        self.maxInactiveInterval = interval

    def getMaxInactiveInterval(self) -> int:
        return self.maxInactiveInterval

    def getSessionContext(self):
        raise ValueError("UnsupportedOperationException(getSessionContext")

    def getAttribute(self, name: str):
        self.assertIsValid()
        assert name is not None, "Attribute name must not be null"
        return self.attributes.get(name)

    def getValue(self, name: str):
        return self.getAttribute(name)

    def getAttributeNames(self) -> list:
        self.assertIsValid()
        return list(self.attributes.keys())

    def getValueNames(self) -> list:
        self.assertIsValid()
        return list(self.attributes.keys())

    def setAttribute(self, name: str, value=None) -> None:
        self.assertIsValid()
        assert name is not None, "Attribute name must not be null"
        if value is None:
            self.removeAttribute(name)
        else:
            oldValue = self.attributes.get(name)
            if oldValue != value:
                if isinstance(oldValue, HttpSessionBindingListener):
                    oldValue.valueUnbound(HttpSessionBindingEvent(self, name, oldValue))
                if isinstance(value, HttpSessionBindingListener):
                    value.valuebound(HttpSessionBindingEvent(self, name, value))

    def putValue(self, name: str, value) -> None:
        self.setAttribute(name, value)

    def removeAttribute(self, name: str) -> None:
        self.assertIsValid()
        assert name is not None, "Attribute name must not be null"
        value = self.attributes.pop(name)
        if isinstance(value, HttpSessionBindingListener):
            value.valueUnbound(HttpSessionBindingEvent(self, name, value))

    def removeValue(self, name: str) -> None:
        self.removeAttribute(name)

    def clearAttributes(self) -> None:
        for name, value in self.attributes.items():
            if isinstance(value, HttpSessionBindingListener):
                value.valuebound(HttpSessionBindingEvent(self, name, value))
        self.attributes.clear()

    def invalidate(self) -> None:
        self.assertIsValid()
        self.invalid = True
        self.clearAttributes()

    def isInvalid(self) -> bool:
        return self.invalid

    def assertIsValid(self) -> None:
        assert (not self.isInvalid), "The session has already been invalidated"

    def setNew(self, value: bool) -> None:
        self.isNew = value

    def isNew(self) -> bool:
        self.assertIsValid()
        return self.isNew

    def serializeState(self):
        state = dict()
        for name, value in self.attributes.items():
            if isinstance(value, Serializable):
                state[name] = value
            elif isinstance(value, HttpSessionBindingListener):
                value.valueUnbound(HttpSessionBindingListener(self, name, value))

        self.attributes.clear()
        return state

    def deserializeState(self, state: Serializable) -> None:
        assert isinstance(state, dict), "Serialized state needs to be of type [java.util.Map]");
        self.attributes.update(state)










