from springframework.beans.factory.config import BeanDefinitionInterface
from springframework.beans.factory.xml import BeanDefinitionParser, ParserContext
from xml.etree.ElementTree import Element

# below no implement
from springframework.beans.factory import BeanDefinitionStoreException
from springframework.beans.factory.config import BeanDefinitionHolder
from springframework.beans.factory.parsing import BeanComponentDefinition
from springframework.beans.factory.support import AbstractBeanDefinition, BeanDefinitionReaderUtils, BeanDefinitionRegistry


class AbstractBeanDefinitionParser(BeanDefinitionParser):

    def __init__(self):
        self.ID_ATTRIBUTE = "id"
        self.NAME_ATTRIBUTE = "name"

    def parse(self, element: Element, parserContext: ParserContext) -> BeanDefinitionInterface:
        definition = self.parseInternal(element, parserContext)
        if (definition is not None) and (not parserContext.isNested()):
            try:
                pass
            except BeanDefinitionStoreException as e:
                msg = getattr(e, 'message', repr(e))
                parserContext.getReaderContext().error(msg, element)

        return definition

    def resolveId(self, element, definition, parserContext) -> str:
        if(self.shouldGenerateId()):
            return parserContext.getReaderContext().generateBeanName(definition)
        else:
            Id = getattr(element, "ID_ATTRIBUTE")
            if (not Id) and self.shouldGenerateIdAsFallback():
                Id = parserContext.getReaderContext().generateBeanName(definition)
            return Id

    def registerBeanDefinition(self, definition, registry):
        # TODO
        BeanDefinitionReaderUtils.registerBeanDefinition(definition, registry)

    def parseInternal(self, element, parserContext):
        raise NotImplementedError

    def shouldGenerateId(self):
        return False

    def shouldGenerateIdAsFallback(self):
        return False

    def shouldParseNameAsAliases(self):
        return True

    def shouldFireEvents(self):
        return True

    def postProcessComponentDefinition(self, componentDefinition):
        pass
