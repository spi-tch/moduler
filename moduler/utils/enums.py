from enum import Enum


class BaseEnum(str, Enum):
    ...


class ModuleType(BaseEnum):
    LINEAR = "linear"
    CONV2D = "conv2d"
    MAXPOOL2D = "maxpool2d"
