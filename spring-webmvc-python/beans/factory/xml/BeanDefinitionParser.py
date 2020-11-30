from beans.factory.config import BeanDefinition
from beans.factory.xml import ParseContext
from xml.etree.ElementTree import Element

class BeanDefinitionParser():
       
    def parse(self, element: Element, parseContext: ParseContext) -> BeanDefinition:
        raise NotImplementedError