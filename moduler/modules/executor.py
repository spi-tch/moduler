import os
from threading import Event

import grpc
from grpc._channel import _InactiveRpcError

from moduler.proto.service_pb2 import Request, Response
from moduler.proto.service_pb2_grpc import ModuleStub

GRPC_ADDRESS = "grpc.babs.ai"


class Executor(object):

    _instance: "Executor" = None
    _busy: Event = Event()

    def __new__(cls):
        if getattr(cls, "_instance") is None:

            key = os.environ.get("BABS_API_KEY")
            if key is None:
                raise ValueError(f"Environment variable BABS_API_KEY not set.")

            cls._instance = super(Executor, cls).__new__(cls)

            # todo: switch to secure channel
            cls._instance.channel = grpc.insecure_channel(
                target=GRPC_ADDRESS,
                options=[('grpc.enable_http_proxy', 0)],
                compression=None,
            )
            cls._instance.stub = ModuleStub(cls._instance.channel)

        return cls._instance

    def execute(self, request: Request) -> Response:
        if self._busy.is_set():
            raise RuntimeError("Executor is currently busy. You can only execute one request at a time.")
        self._busy.set()
        try:
            response = self.stub.execute(request)
            return response

        except _InactiveRpcError as i:
            raise Exception(i.args[0].details)
        finally:
            self._busy.clear()

    def abort(self):
        self._busy.clear()
        self.stub.execute(Request(type=Request.Type.ABORT))
        self.channel.close()
