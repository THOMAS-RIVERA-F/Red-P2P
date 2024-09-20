# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# NO CHECKED-IN PROTOBUF GENCODE
# source: node.proto
# Protobuf Python Version: 5.27.2
"""Generated protocol buffer code."""
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import runtime_version as _runtime_version
from google.protobuf import symbol_database as _symbol_database
from google.protobuf.internal import builder as _builder
_runtime_version.ValidateProtobufRuntimeVersion(
    _runtime_version.Domain.PUBLIC,
    5,
    27,
    2,
    '',
    'node.proto'
)
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\nnode.proto\x12\x04node\"9\n\x0e\x43\x61ncionRequest\x12\x0f\n\x07\x63\x61ncion\x18\x01 \x01(\t\x12\x16\n\x0etamano_cancion\x18\x02 \x01(\x05\" \n\x0fMessageResponse\x12\r\n\x05reply\x18\x01 \x01(\t\"\x1b\n\rNodeIDRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"K\n\x11SuccessorResponse\x12\x19\n\x11successor_address\x18\x01 \x01(\t\x12\x1b\n\x13predecessor_address\x18\x02 \x01(\t\"O\n\rUpdateRequest\x12\x1f\n\x17new_predecessor_address\x18\x01 \x01(\t\x12\x1d\n\x15new_successor_address\x18\x02 \x01(\t\"\x0f\n\rEmptyResponse\"&\n\x18ResponsabilidadesRequest\x12\n\n\x02id\x18\x01 \x01(\x05\"\x84\x01\n\x19ResponsabilidadesResponse\x12\x39\n\x05items\x18\x01 \x03(\x0b\x32*.node.ResponsabilidadesResponse.ItemsEntry\x1a,\n\nItemsEntry\x12\x0b\n\x03key\x18\x01 \x01(\x05\x12\r\n\x05value\x18\x02 \x01(\t:\x02\x38\x01\x32\xe0\x02\n\x0bNodeService\x12:\n\x0bSendMessage\x12\x14.node.CancionRequest\x1a\x15.node.MessageResponse\x12=\n\rFindSuccessor\x12\x13.node.NodeIDRequest\x1a\x17.node.SuccessorResponse\x12=\n\x11UpdatePredecessor\x12\x13.node.UpdateRequest\x1a\x13.node.EmptyResponse\x12;\n\x0fUpdateSuccessor\x12\x13.node.UpdateRequest\x1a\x13.node.EmptyResponse\x12Z\n\x17\x42uscarResponsabilidades\x12\x1e.node.ResponsabilidadesRequest\x1a\x1f.node.ResponsabilidadesResponseb\x06proto3')

_globals = globals()
_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, _globals)
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, 'node_pb2', _globals)
if not _descriptor._USE_C_DESCRIPTORS:
  DESCRIPTOR._loaded_options = None
  _globals['_RESPONSABILIDADESRESPONSE_ITEMSENTRY']._loaded_options = None
  _globals['_RESPONSABILIDADESRESPONSE_ITEMSENTRY']._serialized_options = b'8\001'
  _globals['_CANCIONREQUEST']._serialized_start=20
  _globals['_CANCIONREQUEST']._serialized_end=77
  _globals['_MESSAGERESPONSE']._serialized_start=79
  _globals['_MESSAGERESPONSE']._serialized_end=111
  _globals['_NODEIDREQUEST']._serialized_start=113
  _globals['_NODEIDREQUEST']._serialized_end=140
  _globals['_SUCCESSORRESPONSE']._serialized_start=142
  _globals['_SUCCESSORRESPONSE']._serialized_end=217
  _globals['_UPDATEREQUEST']._serialized_start=219
  _globals['_UPDATEREQUEST']._serialized_end=298
  _globals['_EMPTYRESPONSE']._serialized_start=300
  _globals['_EMPTYRESPONSE']._serialized_end=315
  _globals['_RESPONSABILIDADESREQUEST']._serialized_start=317
  _globals['_RESPONSABILIDADESREQUEST']._serialized_end=355
  _globals['_RESPONSABILIDADESRESPONSE']._serialized_start=358
  _globals['_RESPONSABILIDADESRESPONSE']._serialized_end=490
  _globals['_RESPONSABILIDADESRESPONSE_ITEMSENTRY']._serialized_start=446
  _globals['_RESPONSABILIDADESRESPONSE_ITEMSENTRY']._serialized_end=490
  _globals['_NODESERVICE']._serialized_start=493
  _globals['_NODESERVICE']._serialized_end=845
# @@protoc_insertion_point(module_scope)
