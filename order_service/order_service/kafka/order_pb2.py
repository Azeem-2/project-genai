# -*- coding: utf-8 -*-
# Generated by the protocol buffer compiler.  DO NOT EDIT!
# source: .proto
"""Generated protocol buffer code."""
from google.protobuf.internal import builder as _builder
from google.protobuf import descriptor as _descriptor
from google.protobuf import descriptor_pool as _descriptor_pool
from google.protobuf import symbol_database as _symbol_database
# @@protoc_insertion_point(imports)

_sym_db = _symbol_database.Default()




DESCRIPTOR = _descriptor_pool.Default().AddSerializedFile(b'\n\x06.proto\x12\x05order\"O\n\x0bOrderCreate\x12\x0f\n\x07user_id\x18\x01 \x01(\x05\x12\x1a\n\x05items\x18\x02 \x03(\x0b\x32\x0b.order.Item\x12\x13\n\x0btotal_price\x18\x03 \x01(\x02\",\n\x04Item\x12\x12\n\nproduct_id\x18\x01 \x01(\x05\x12\x10\n\x08quantity\x18\x02 \x01(\x05\"[\n\x0bOrderUpdate\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x0f\n\x07user_id\x18\x02 \x01(\x05\x12\x1a\n\x05items\x18\x03 \x03(\x0b\x32\x0b.order.Item\x12\x13\n\x0btotal_price\x18\x04 \x01(\x02\"U\n\x0fOrderItemUpdate\x12\n\n\x02id\x18\x01 \x01(\x05\x12\x10\n\x08order_id\x18\x02 \x01(\x05\x12\x12\n\nproduct_id\x18\x03 \x01(\x05\x12\x10\n\x08quantity\x18\x04 \x01(\x05\x62\x06proto3')

_builder.BuildMessageAndEnumDescriptors(DESCRIPTOR, globals())
_builder.BuildTopDescriptorsAndMessages(DESCRIPTOR, '_pb2', globals())
if _descriptor._USE_C_DESCRIPTORS == False:

  DESCRIPTOR._options = None
  _ORDERCREATE._serialized_start=17
  _ORDERCREATE._serialized_end=96
  _ITEM._serialized_start=98
  _ITEM._serialized_end=142
  _ORDERUPDATE._serialized_start=144
  _ORDERUPDATE._serialized_end=235
  _ORDERITEMUPDATE._serialized_start=237
  _ORDERITEMUPDATE._serialized_end=322
# @@protoc_insertion_point(module_scope)
