# Generated by the gRPC Python protocol compiler plugin. DO NOT EDIT!
"""Client and server classes corresponding to protobuf-defined services."""
import grpc
import warnings

import node_pb2 as node__pb2

GRPC_GENERATED_VERSION = '1.66.1'
GRPC_VERSION = grpc.__version__
_version_not_supported = False

try:
    from grpc._utilities import first_version_is_lower
    _version_not_supported = first_version_is_lower(GRPC_VERSION, GRPC_GENERATED_VERSION)
except ImportError:
    _version_not_supported = True

if _version_not_supported:
    raise RuntimeError(
        f'The grpc package installed is at version {GRPC_VERSION},'
        + f' but the generated code in node_pb2_grpc.py depends on'
        + f' grpcio>={GRPC_GENERATED_VERSION}.'
        + f' Please upgrade your grpc module to grpcio>={GRPC_GENERATED_VERSION}'
        + f' or downgrade your generated code using grpcio-tools<={GRPC_VERSION}.'
    )


class NodeServiceStub(object):
    """Definición del servicio de Node
    """

    def __init__(self, channel):
        """Constructor.

        Args:
            channel: A grpc.Channel.
        """
        self.SendMessage = channel.unary_unary(
                '/node.NodeService/SendMessage',
                request_serializer=node__pb2.CancionRequest.SerializeToString,
                response_deserializer=node__pb2.MessageResponse.FromString,
                _registered_method=True)
        self.FindSuccessor = channel.unary_unary(
                '/node.NodeService/FindSuccessor',
                request_serializer=node__pb2.NodeIDRequest.SerializeToString,
                response_deserializer=node__pb2.SuccessorResponse.FromString,
                _registered_method=True)
        self.UpdatePredecessor = channel.unary_unary(
                '/node.NodeService/UpdatePredecessor',
                request_serializer=node__pb2.UpdateRequest.SerializeToString,
                response_deserializer=node__pb2.EmptyResponse.FromString,
                _registered_method=True)
        self.UpdateSuccessor = channel.unary_unary(
                '/node.NodeService/UpdateSuccessor',
                request_serializer=node__pb2.UpdateRequest.SerializeToString,
                response_deserializer=node__pb2.EmptyResponse.FromString,
                _registered_method=True)
        self.BuscarResponsabilidades = channel.unary_unary(
                '/node.NodeService/BuscarResponsabilidades',
                request_serializer=node__pb2.ResponsabilidadesRequest.SerializeToString,
                response_deserializer=node__pb2.ResponsabilidadesResponse.FromString,
                _registered_method=True)
        self.BuscarCancion = channel.unary_unary(
                '/node.NodeService/BuscarCancion',
                request_serializer=node__pb2.BuscarCancionRequest.SerializeToString,
                response_deserializer=node__pb2.BuscarCancionResponse.FromString,
                _registered_method=True)


class NodeServiceServicer(object):
    """Definición del servicio de Node
    """

    def SendMessage(self, request, context):
        """Método para enviar mensajes entre nodos
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def FindSuccessor(self, request, context):
        """Método para encontrar el sucesor de un nodo en la red
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdatePredecessor(self, request, context):
        """Métodos para actualizar el predecesor y el sucesor de un nodo (Join)
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def UpdateSuccessor(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BuscarResponsabilidades(self, request, context):
        """Missing associated documentation comment in .proto file."""
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')

    def BuscarCancion(self, request, context):
        """RPC para buscar una canción en la red
        """
        context.set_code(grpc.StatusCode.UNIMPLEMENTED)
        context.set_details('Method not implemented!')
        raise NotImplementedError('Method not implemented!')


def add_NodeServiceServicer_to_server(servicer, server):
    rpc_method_handlers = {
            'SendMessage': grpc.unary_unary_rpc_method_handler(
                    servicer.SendMessage,
                    request_deserializer=node__pb2.CancionRequest.FromString,
                    response_serializer=node__pb2.MessageResponse.SerializeToString,
            ),
            'FindSuccessor': grpc.unary_unary_rpc_method_handler(
                    servicer.FindSuccessor,
                    request_deserializer=node__pb2.NodeIDRequest.FromString,
                    response_serializer=node__pb2.SuccessorResponse.SerializeToString,
            ),
            'UpdatePredecessor': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdatePredecessor,
                    request_deserializer=node__pb2.UpdateRequest.FromString,
                    response_serializer=node__pb2.EmptyResponse.SerializeToString,
            ),
            'UpdateSuccessor': grpc.unary_unary_rpc_method_handler(
                    servicer.UpdateSuccessor,
                    request_deserializer=node__pb2.UpdateRequest.FromString,
                    response_serializer=node__pb2.EmptyResponse.SerializeToString,
            ),
            'BuscarResponsabilidades': grpc.unary_unary_rpc_method_handler(
                    servicer.BuscarResponsabilidades,
                    request_deserializer=node__pb2.ResponsabilidadesRequest.FromString,
                    response_serializer=node__pb2.ResponsabilidadesResponse.SerializeToString,
            ),
            'BuscarCancion': grpc.unary_unary_rpc_method_handler(
                    servicer.BuscarCancion,
                    request_deserializer=node__pb2.BuscarCancionRequest.FromString,
                    response_serializer=node__pb2.BuscarCancionResponse.SerializeToString,
            ),
    }
    generic_handler = grpc.method_handlers_generic_handler(
            'node.NodeService', rpc_method_handlers)
    server.add_generic_rpc_handlers((generic_handler,))
    server.add_registered_method_handlers('node.NodeService', rpc_method_handlers)


 # This class is part of an EXPERIMENTAL API.
class NodeService(object):
    """Definición del servicio de Node
    """

    @staticmethod
    def SendMessage(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/node.NodeService/SendMessage',
            node__pb2.CancionRequest.SerializeToString,
            node__pb2.MessageResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def FindSuccessor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/node.NodeService/FindSuccessor',
            node__pb2.NodeIDRequest.SerializeToString,
            node__pb2.SuccessorResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdatePredecessor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/node.NodeService/UpdatePredecessor',
            node__pb2.UpdateRequest.SerializeToString,
            node__pb2.EmptyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def UpdateSuccessor(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/node.NodeService/UpdateSuccessor',
            node__pb2.UpdateRequest.SerializeToString,
            node__pb2.EmptyResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def BuscarResponsabilidades(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/node.NodeService/BuscarResponsabilidades',
            node__pb2.ResponsabilidadesRequest.SerializeToString,
            node__pb2.ResponsabilidadesResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)

    @staticmethod
    def BuscarCancion(request,
            target,
            options=(),
            channel_credentials=None,
            call_credentials=None,
            insecure=False,
            compression=None,
            wait_for_ready=None,
            timeout=None,
            metadata=None):
        return grpc.experimental.unary_unary(
            request,
            target,
            '/node.NodeService/BuscarCancion',
            node__pb2.BuscarCancionRequest.SerializeToString,
            node__pb2.BuscarCancionResponse.FromString,
            options,
            channel_credentials,
            insecure,
            call_credentials,
            compression,
            wait_for_ready,
            timeout,
            metadata,
            _registered_method=True)
