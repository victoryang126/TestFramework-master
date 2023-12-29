import struct
from typing import Tuple, List

class FileHeaderStruct:
    def __init__(self, data):
        self.signature, \
        self.header_size, \
        self.app_id, \
        self.app_major, \
        self.app_minor, \
        self.app_build, \
        self.bin_log_major, \
        self.bin_log_minor, \
        self.bin_log_build, \
        self.bin_log_patch, \
        self.file_size, \
        self.uncompressed_size, \
        self.obj_count, \
        self.obj_count_read, \
        *self.app_version, \
        *self.bin_log_version = struct.unpack("<4sLBBBBBBBBQQLL8H8H", data)

class ObjHeaderBaseStruct:
    def __init__(self, data):
        self.signature, \
        self.header_size, \
        self.header_version, \
        self.obj_size, \
        self.obj_type = struct.unpack("<4sHHLL", data)

class ObjHeaderV1Struct:
    def __init__(self, data):
        self.flags, \
        self.client_index, \
        self.obj_version, \
        self.timestamp = struct.unpack("<LHHQ", data)

class ObjHeaderV2Struct:
    def __init__(self, data):
        self.flags, \
        self.timestamp_status, \
        self.obj_version, \
        self.timestamp = struct.unpack("<LBxHQ8x", data)

class LogContainerStruct:
    def __init__(self, data):
        self.compression_method, \
        self.size_uncompressed = struct.unpack("<H6xL4x", data)

class CanMsgStruct:
    def __init__(self, data):
        self.channel, \
        self.flags, \
        self.dlc, \
        self.arbitration_id, \
        self.data = struct.unpack("<HBBL8s", data)

class CanFdMsgStruct:
    def __init__(self, data):
        self.channel, \
        self.flags, \
        self.dlc, \
        self.arbitration_id, \
        _, \
        _, \
        self.fd_flags, \
        self.valid_bytes, \
        self.data = struct.unpack("<HBBLLBBB5x64s", data)

class CanFdMsg64Struct:
    def __init__(self, data):
        self.channel, \
        self.dlc, \
        self.valid_bytes, \
        _, \
        self.arbitration_id, \
        _, \
        self.fd_flags, \
        _, \
        _, \
        _, \
        _, \
        _, \
        self.direction, \
        _, \
        _, = struct.unpack("<BBBBLLLLLLLHBBL", data)

class CanErrorExtStruct:
    def __init__(self, data):
        self.channel, \
        self.dlc, \
        self.valid_payload_length, \
        _, \
        self.arbitration_id, \
        _, \
        self.fd_flags, \
        _, \
        _, \
        _, \
        _, \
        _, \
        _, \
        self.ecc, \
        self.position, \
        self.data = struct.unpack("<HHLBBBxLLH2x8s", data)
