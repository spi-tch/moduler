import torch
import torch.nn as nn

from moduler.modules.executor import Executor
from moduler.proto.commons_pb2 import Tensor
from moduler.proto.service_pb2 import Request
from moduler.utils.enums import ModuleType
from moduler.utils.misc import convert_to_str_dict


class Module(nn.Module):

    _id: str
    executor: Executor = Executor()

    def __init__(self, module_type: ModuleType = None, **kwargs):
        super().__init__()
        if module_type is not None:
            self.register(module_type, **kwargs)

    def forward(self, input: torch.Tensor) -> torch.Tensor:
        input = input.detach()
        tensor: Tensor = Tensor(        # todo: add compression
            buffer=input.numpy().tobytes(),
            size=input.shape,
            dtype=str(input.dtype).replace("torch.", ""),
        )
        request = Request(
            type=Request.Type.FORWARD,
            module_id=self._id,
            tensor=tensor
        )
        try:
            tensor = self.executor.execute(request=request).tensor
        except Exception as e:
            raise e
        size = list(tensor.size)
        return torch.frombuffer(tensor.buffer, dtype=getattr(torch, tensor.dtype)).view(size)

    def register(self, module_type: ModuleType, **kwargs):
        weight = kwargs.pop("weight", None)
        kwargs.update({"module_type": module_type.value})
        kwargs_str = convert_to_str_dict(kwargs)
        request = Request(
            type=Request.Type.REGISTER_MODULE,
            parameters=kwargs_str,
            tensor=weight,
        )
        self._id = self.executor.execute(request=request).module_id
