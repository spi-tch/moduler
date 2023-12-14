from moduler.modules import Module
from moduler.utils.enums import ModuleType


class Stack(Module):

    # todo: complete this module
    def __init__(self, modules: list[dict[ModuleType, dict[str, any]]]):
        super().__init__(None)
        for module in modules:
            self.register(module)
