from springframework.context.ConfigurableApplicationContext import ConfigurableApplicationContext
from springframework.core.io.DefaultResourceLoader import DefaultResourceLoader


class AbstractApplicationContext(
    DefaultResourceLoader,
    ConfigurableApplicationContext
):

    def set_display_name(self, displayName: str):
        assert displayName, "Display name must not be empty"
        self.displayName = displayName
