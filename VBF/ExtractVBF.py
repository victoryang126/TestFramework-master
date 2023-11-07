import os
import re
import eel


# VBF 格式 通过读出来的格式
# # b'vbf_version = 2.6;\r\n'
# b'header {\r\n'
# b'\t// Created by VbfSign build: 2017/12/12 on 2019/6/14 10:38\r\n'
# b'\tsw_part_number = "AlgoVar1FixedCal";\r\n'
# b'\tsw_version = "AA";\r\n'
# b'\tsw_part_type  = EXE;\r\n'
# b'\tdata_format_identifier = 0x00;\r\n'
# b'\tecu_address = 0x1C01;\r\n'
# b'\tfile_checksum = 0x130475CA;\r\n'
# b'\terase = {{0xA0020000,0x00008000 }};\r\n'
# b'\tverification_block_start = 0xA0027F20;\r\n'
# b'\tverification_block_length = 0x0000002C;\r\n'
# b'\tverification_block_root_hash = 0xA7B7B55EE19D8CF18FB854DD02D1195D20EE742242B2BAABE21E0F1DED4525D8;\r\n'
# b'\tsw_signature_dev = 0x991986E9DD3A7657104860047DD228F700F262885AACBF77D5C470AAE1D43AD95687AEB466572EA54E4402CE3634AD55807860BF936CCE8F44F9DC2D64B16C013827B7DE884D328E11BCA5841E2CCB514B914147BE6F48DD329B011AAE67F965F741F19BF8FC5864A26CD96C4353A8E19AEE66B750566448AAA467369ECB6B779FDCC015E62197FA385F58253D7B215C61F88F5C08707A75E8F237D7BDC1613B5E22C5CBDC4611CF12CED81D7D02056FBE1011AB17B46AD0B5A1009606C3D35C8D650CF84FA3B6C9C49F46644E30588D5B62623E42A0EB32BFFBA390D7D76E10E471A7D8C21A96B9094F8BBF4122142E4A2B615C705432B41DB531F2E893D26C;\r\n'
# b'}\xa0\x02\x00\x00\x00\x00\x7f\x00\  这里是'} + 4byte startaddress + 4byte length
# 然后后面是所有的数据内容 + 2byte 的 第一个Block CheckSum
# 再接着是verification block 的4byte startaddress + 4byte length +2byte 的 第二个Block CheckSum


class Vbf(object):
    def __init__(self, VBFPath):
        self.VBFPath = VBFPath
        self.Call = ""
        self.DataBlock_Length = ""
        self.DataBlock_StAddr = ""
        self.EraseStart = ""
        self.EraseEnd = ""
        self.VFBlock_StAddr = ""
        self.VFBlock_Length = ""
        self.Signature_Dev = ""
        self.DataBlock = []
        self.VFBlock = []

        with open(self.VBFPath, "rb") as fd:
            IsHeader = True
            IsVFBlock = False
            VFBlock_Offset = 10  # check sum:2bytes start_addr=4 bytes  length=4bytes
            DB_Length = 0
            VFB_Length = 0
            for line in fd.readlines():
                if line[0] == 0x7D:  # reach }
                    # byte = hex(line[0])
                    # print(type(byte))
                    IsHeader = False
                    # self.DataBlock_StAddr = int.from_bytes(line[1:5], byteorder="big")
                    self.DataBlock_StAddr = hex(int.from_bytes(line[1:5], byteorder="big"))
                    self.DataBlock_Length = int.from_bytes(line[5:9], byteorder="big")
                    DB_Length = self.DataBlock_Length
                    self.DataBlock_Length = hex(self.DataBlock_Length)
                    line = line[9:]  # discard the start address and length

                # parse header
                if (IsHeader):
                    pass
                    line = re.sub(r'[\s;]', "", line.decode("utf-8"))
                    if "sw_part_number" in line:
                        print( line.split('=')[1].rstrip(';'))
                    if "call" in line:
                        self.Call = line.split('=')[1].rstrip(';')
                    elif "verification_block_start" in line:
                        self.VFBlock_StAddr = line.split('=')[1]
                        # self.verif_start_addr = int(self.verif_start_addr,16)
                    elif "verification_block_length" in line:
                        self.VFBlock_Length = line.split('=')[1]

                        VFB_Length = int(self.VFBlock_Length, 16)
                    elif "sw_signature_dev" in line:
                        self.Signature_Dev = line.split('=')[1]
                        # self.Signature_Dev = int(self.Signature_Dev, 16).to_bytes(256, byteorder="big")
                    elif "sw_signature" in line:
                        self.Signature = line.split('=')[1].strip().rstrip(';')
                        self.Signature = int(self.Signature, 16).to_bytes(256, byteorder="big")
                    elif "erase" in line:
                        Reg_Erase = re.compile('(?<=erase={{)[\w,]*')
                        self.EraseStart, self.EraseEnd = re.findall(Reg_Erase, line)[0].split(',')

                # parse content 获取到了data段段数据
                else:
                    for byte in bytes(line):
                        byte = hex(byte)[2:]
                        if (len(byte) == 1):
                            byte = '0' + byte

                        DB_Length -= 1  # 获取一次data block的length -1
                        if DB_Length >= 0:  # parce sw part 如果长度还是大于等于0 则还是data段
                            self.DataBlock.append(byte)
                        else:  # parse verification table  否则就是verification block data
                            VFBlock_Offset -= 1
                            if (VFBlock_Offset < 0):  # consume all 10 bytes offset
                                IsVFBlock = True
                            if IsVFBlock:
                                VFB_Length -= 1
                                if VFB_Length >= 0:
                                    self.VFBlock.append(byte)

            def GetVBFCall(self):
                return self.Call

            @eel.expose
            def GetDB_StAddr(self):
                return self.DataBlock_StAddr

            def GetDB_Length(Self):
                return self.DataBlock_Length

            def GetVFB_StAddr(self):
                return self.VFBlock_StAddr

            def GetVFB_Length(self):
                return self.VFBlock_Length

            def GetSignature_Dev(self):
                return self.Signature_Dev

            def GetDB_Data(self):
                return self.DataBlock

            def GetVFB_Data(self):
                return self.VFBlock

                # self.Call = ""
                # self.DataBlock_Length = ""
                # self.DataBlock_StAddr = ""
                # self.EraseStart = ""
                # self.EraseEnd = ""
                # self.VFBlock_StAddr = ""
                # self.VFBlock_Length = ""
                # self.Signature_Dev = ""
                # self.DataBlock = []
                # self.VFBlock = []
            # 处理数据成一个字符串
            # self.DB = "".join(self.DataBlock)
            # self.DB = int.from_bytes(self.DataBlock[:],byteorder="big") 不行
            # self.VB = ''.join(self.VFBlock)


Vtest = Vbf('Application_Signed.vbf')
# print(Vtest.DataBlock,Vtest.DataBlock_Length)
print(Vtest.EraseStart,Vtest.EraseEnd)
print(Vtest.Call,len(Vtest.Call))
print(Vtest)
# print(Vtest.__dict__)