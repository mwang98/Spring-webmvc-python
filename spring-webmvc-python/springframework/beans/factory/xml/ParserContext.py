from springframework.beans.factory.config import BeanDefinitionInterface
#from beans.factory.parsing import *


class ParserContext():

    def __init__(self, readerContext, delegate, containingBeanDefinition=None):
        self._readerContext = readerContext
        self._delegate = delegate
        self._containingBeanDefinition = containingBeanDefinition
        self._containingComponents = list()  # deque

    def getReaderContext(self):
        return self._readerContext

    def getRegistry(self):
        return self._readerContext.getRegistry()

    def getDelegate(self):
        return self._delegate

    def getContainingBeanDefinition(self):
        return self._containingBeanDefinition

    def isNested(self):
        return (self._containingBeanDefinition is not None)

    def isDefaultLazyInit(self):
        # TODO
        pass

    def extractSource(self, sourceCandidate):
        return self._readerContext.extractSource(sourceCandidate)

    def getContainingComponent(self):
        return self.containingComponents.peek()

    def pushContainingComponent(self, containingComponent):
        self._containingComponents.push(containingComponent)

    def popAndRegisterContainingComponent(self, containingComponent):
        self.registerComponent(self.popContainingComponent())

    def registerComponent(self, component):
        containingComponent = self.getContainingComponent()
        if containingComponent is not None:
            containingComponent.addNestedComponent(component)
        else:
            self._readerContext.fireComponentRegistered(component)

    def registerBeanComponent(self, component):
        #  TODO
        # BeanDefinitionReaderUtils.registerBeanDefinition(component, self.getRegistry())
        self.registerComponent(component)

        