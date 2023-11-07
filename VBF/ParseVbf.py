import argparse
import re
from binascii import unhexlify, hexlify


"""
vbf_version = 2.6;
header {
	// Created by VbfSign build: 2017/12/12 on 2019/6/14 10:38
	sw_part_number = "Application";
	sw_version = "AA";
	sw_part_type  = EXE;
	data_format_identifier = 0x00;
	ecu_address = 0x1C01;
	file_checksum = 0x141776FE;
	erase = {{0xA0040000,0x000C0000 }};
	verification_block_start = 0xA00FFF20;
	verification_block_length = 0x0000002C;
	verification_block_root_hash = 0x9202AA095418E46828581DD4E23A934586FCAB6116F4503DF2472B433A93CC8E;
	sw_signature_dev = 0x1C2DCE77D72B96E3BC5E0A759C74BE00215A53A01788290061C00E4BF18A5E019532E93400A86F91A5AAEBDB4F402FFBE6031374331960079466E99A4E9B97E0B48BBC6381A50C50D0D7A3B6C8AFCBCB93FA55E735A0D59ACFABB30C177DB13AC81D6657F94CC1C9B3F25F07E83EF9DCF1FFCB2E85C1007735272A2DDC918D6545D098965A0B82D4FD6894729AA575B3A38B66964AEDDD3FCC9A00671DD0628D904A953C822B1046333C4E062AFCAD6E49A98FDD99074EC96E9052D4101075BFE2EBAC5266E2F138900888CCB94083D76F3AA7627C18E667F8E8BCF2DEF71BF3DB0F8501BD3E476212F185D270CE350A9CCB62389958F2FA454F39D530FA66A3;
}data
"""
class VBF:


    def __init__(self, file):
        self.version:float = 0
        self.description:str = ""
        self.sw_part:str = ""
        self.sw_part_type:str = ""
        self.data_format_identifier = 0x00
        self.verification_block_start = 0x00

        self.erase = []
        self.checksum = bytes()

        self.data = []
        self.sw_signature_dev = ""
        self.block:int = 0
        self.header = bytes()

        with open(file, "rb") as fd:
            data = fd.read()
        try:
            'sw_version = "AA";'
            self.version = data[data.find(b"vbf_version"):data.find(b"\n")].split(b"=")[1].replace(b" ", b"").replace(b";", b"").decode()
        except:
            raise ValueError("Version not found")

        self.header = data[data.find(b"header"):data.find(b"\n}")+2]


        erase_flag = False
        # for line in self.header.split(b"\n"):
        #     line = re.sub(r'[\s;]', "", line.decode("utf-8"))
        #     print(line)
        #     if line.startswith("//"):
        #         continue
        #     if "sw_part_number" in line:
        #         self.sw_part = line.split('=')[1].rstrip(';').replace("\"", "")
        #         #'sw_part_number = "Application";'
        #         # self.sw_part = line[line.find(b" = ")+3:line.find(b"\";")].replace(b" ", b"").replace(b"\"", b"").decode()
        #         # print(self.sw_part)
            # if b"sw_part_type" in line:
            #     #'sw_part_type  = EXE;'
            #     self.sw_part_type = line[line.find(b" = ")+3:line.find(b";")].replace(b" ", b"").replace(b"\"", b"").decode()
            # if b"data_format_identifier" in line:
            #     #'data_format_identifier = 0x00;'
            #     self.data_format_identifier = int(line[line.find(b" = ")+3:line.find(b";")].replace(b" ", b"").replace(b"\"", b"").decode(), 16)
            # if b"verification_block_start" in line:
            #     #'verification_block_start = 0xA00FFF20;'
            #     self.verification_block_start = int(line[line.find(b" = 0x")+5:line.find(b";")].replace(b" ", b"").replace(b"\"", b"").decode(), 16)
            # if b"file_checksum" in line:
            #     #'file_checksum = 0x141776FE;'
            #     self.file_checksum = unhexlify(line[line.find(b" = 0x")+5:line.find(b";")].replace(b" ", b"").replace(b"\"", b""))
            # if b"sw_signature_dev" in line:
            #     #'sw_signature_dev = 0x1C2DCE77D72B96E3BC5E0A759C74BE001960079466E99A4E9B9...;'
            #     self.sw_signature_dev = unhexlify(line[line.find(b" = 0x")+5:line.find(b";")].replace(b" ", b"").replace(b"\"", b""))
            # if b"erase = " in line or erase_flag:
            #     #'erase = {{0xA0040000, 0x000C0000}};'
            #     erase_flag = True
            #     r = re.compile(r'{\s*0x([0-9A-Fa-f]+),\s*0x([0-9A-Fa-f]+)\s*}')
            #     m = r.search(line.decode())
            #     if m is not None:
            #         self.erase.append([m.group(1), m.group(2)])
            # if erase_flag:
            #     if b"};" in line:
            #         erase_flag = False
        for line in self.header.split(b"\n"):
            line = line.replace(b"\t", b"").replace(b"\r", b"")
            if line.startswith(b"//"):
                continue
            try:
                if b"sw_part_number" in line:
                    #'sw_part_number = "Application";'
                    self.sw_part = line[line.find(b" = ")+3:line.find(b"\";")].replace(b" ", b"").replace(b"\"", b"").decode()
                    # print(self.sw_part)
                if b"sw_part_type" in line:
                    #'sw_part_type  = EXE;'
                    self.sw_part_type = line[line.find(b" = ")+3:line.find(b";")].replace(b" ", b"").replace(b"\"", b"").decode()
                if b"data_format_identifier" in line:
                    #'data_format_identifier = 0x00;'
                    self.data_format_identifier = int(line[line.find(b" = ")+3:line.find(b";")].replace(b" ", b"").replace(b"\"", b"").decode(), 16)
                if b"verification_block_start" in line:
                    #'verification_block_start = 0xA00FFF20;'
                    self.verification_block_start = int(line[line.find(b" = 0x")+5:line.find(b";")].replace(b" ", b"").replace(b"\"", b"").decode(), 16)
                if b"file_checksum" in line:
                    #'file_checksum = 0x141776FE;'
                    self.file_checksum = unhexlify(line[line.find(b" = 0x")+5:line.find(b";")].replace(b" ", b"").replace(b"\"", b""))
                if b"sw_signature_dev" in line:
                    #'sw_signature_dev = 0x1C2DCE77D72B96E3BC5E0A759C74BE001960079466E99A4E9B9...;'
                    self.sw_signature_dev = unhexlify(line[line.find(b" = 0x")+5:line.find(b";")].replace(b" ", b"").replace(b"\"", b""))
                if b"erase = " in line or erase_flag:
                    #'erase = {{0xA0040000, 0x000C0000}};'
                    erase_flag = True
                    r = re.compile(r'{\s*0x([0-9A-Fa-f]+),\s*0x([0-9A-Fa-f]+)\s*}')
                    m = r.search(line.decode())
                    if m is not None:
                        self.erase= [m.group(1), m.group(2)]
                if erase_flag:
                    if b"};" in line:
                        erase_flag = False
            except Exception as e:
                print(line)
                raise

    # def get_data_block(self):
        binary_offset = data.find(b"\n}")+2
        binary = data[binary_offset:]
        self.data = list()
        while len(binary) > 0:
            location = int.from_bytes(binary[:4], 'big')
            size = int.from_bytes(binary[4:8], 'big')
            data = binary[8:8+size]
            checksum = binary[8+size:8+size+2]
            binary = binary[8+size+2:]
            print("Offset: 0x{:X}, Location: 0x{:X}, Size: 0x{:X}, Data Offset: 0x{:X}".format(binary_offset,  location, size, binary_offset + 8))
            binary_offset += 8+size+2
            if location != self.verification_block_start:
                self.data.append((location, data, checksum))

    def get_header_attributes(self,attr):
        attr_value = None
        for line in self.header.split(b"\n"):
            line = line.replace(b"\t", b"").replace(b"\r", b"")
            if line.startswith(b"//"):
                continue
            if attr.encode() in line:
                attr_value = line[line.find(b" = ") + 3:line.find(b"\";")]\
                    .replace(b" ", b"")\
                    .replace(b"\"",b"").decode()
        return attr_value

if __name__ == "__main__":
    # with open('Application_Signed.vbf', "rb") as fd:
    #     datas = fd.read()
    Vtest = VBF("Application_Signed.vbf")
    # print(Vtest.data[1])
    print(Vtest.data_format_identifier)
    print(Vtest.description)
    print(Vtest.erase)
    print(Vtest.file_checksum.hex())
    print(Vtest.sw_signature_dev.hex())