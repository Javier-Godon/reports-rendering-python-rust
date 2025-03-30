import grpc

import app.grpc_client_impl.proto.get_cpu_system_usage_pb2 as grpc_system_proto_contracts
import app.grpc_client_impl.proto.get_cpu_system_usage_pb2_grpc as grpc_system_proto_client
import app.grpc_client_impl.proto.get_cpu_user_usage_pb2 as grpc_user_proto_contracts
import app.grpc_client_impl.proto.get_cpu_user_usage_pb2_grpc as grpc_user_proto_client


class GRPCClient:
    def __init__(self, channel: grpc.Channel):
        self.channel = channel
        self.system_stub = grpc_system_proto_client.GetCpuSystemUsageServiceStub(channel)
        self.user_stub = grpc_user_proto_client.GetCpuUserUsageServiceStub(channel)

    def get_cpu_system_usage(self, date_from, date_to) -> grpc_system_proto_contracts.GetCpuSystemUsageResponse:
        request = grpc_system_proto_contracts.GetCpuSystemUsageRequest(date_from=date_from, date_to=date_to)
        return self.system_stub.GetCpuSystemUsage(request)

    def get_cpu_user_usage(self, date_from, date_to) -> grpc_user_proto_contracts.GetCpuUserUsageResponse:
        request = grpc_user_proto_contracts.GetCpuUserUsageRequest(date_from=date_from, date_to=date_to)
        return self.user_stub.GetCpuUserUsage(request)

class GRPCClientSingleton:
    _instance = None

    @classmethod
    def get_instance(cls):
        if cls._instance is None:
            channel = grpc.insecure_channel("localhost:50051")
            cls._instance = GRPCClient(channel)
        return cls._instance
