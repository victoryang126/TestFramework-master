
import re
from typing import List
from binascii import unhexlify, hexlify
import time

class VBF_Block:

    def __init__(self,start_address,length,data,checksum):
        self.start_address:bytearray = start_address
        self.length:bytearray  = length
        self.data:bytearray = data
        self.checksum:bytearray = checksum

    def __str__(self):
        return(f"start_address :{ self.start_address.hex()} \n "
              f"length: {self.length.hex()}\n"
              f"data length: {len(self.data)}\n"
              f"checksum: {self.checksum.hex()}")

class VBF:

    def __init__(self, file):
        """
        funtion used to parse the Vbf file, it will take about 0.010660886764526367 to the application vbf file,
        so for other file, it will be more faster
        :param file:the path of vbf
        """
        #the header attributes
        self.version:float = 0
        self.description:str = ""
        self.sw_part:str = ""
        self.sw_part_type:str = ""
        self.data_format_identifier:int = 0x00
        self.ecu_address:bytearray = bytearray()
        self.file_checksum:bytearray = bytearray()
        self.call:bytearray = bytearray() #sbl
        self.erase:List[bytearray] = []
        self.verification_block_start:int = 0x00
        self.verification_block_length:int = 0x00
        self.verification_block_root_hash:bytearray = bytearray()
        self.sw_signature_devbytearray = bytearray()

        #user defined data used in other function
        self.binary_header:bytes = bytes()
        self.blocks:List[VBF_Block] = []


        print(time.time())
        try:
            with open(file, "rb") as fd:
                binary_vbf = fd.read()

            #get the binary_header, the foramt:binary_header{}
            self.binary_header = binary_vbf[binary_vbf.find(b"header"):binary_vbf.find(b"\n}") + 2]

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
            for line in self.binary_header.split(b"\n"):
                line = re.sub(r'[\s;]', "", line.decode("utf-8"))#remove space and ;
                if line.startswith("//"):
                    continue
                if "sw_part_number" in line:
                    self.sw_part = line.split('=')[1].replace("\"", "")
                    # print(f"sw_part_number {self.sw_part}")
                if "sw_version" in line:
                    self.sw_version = line.split('=')[1].replace("\"", "")
                    # print(f"sw_version {self.sw_version}")
                if "sw_part_type" in line:
                    self.sw_part_type = line.split('=')[1].replace("\"", "")
                    # print(f"sw_part_type {self.sw_part_type}")
                if "data_format_identifier" in line:
                    self.data_format_identifier =int(line.split('=')[1].replace("\"", ""),16)
                    # print(f"data_format_identifier {self.data_format_identifier}")
                if "ecu_address" in line:
                    self.ecu_address =bytearray.fromhex(line.split('=')[1].replace("\"", "").replace("0x", ""))
                    # print(f"ecu_address {self.ecu_address}")
                if "file_checksum" in line:
                    self.file_checksum = bytearray.fromhex(line.split('=')[1].replace("\"", "").replace("0x", ""))
                if "call" in line:
                    self.call = bytearray.fromhex(line.split('=')[1].replace("\"", "").replace("0x", ""))
                if "erase" in line:
                    r = re.compile(r'{\s*0x([0-9A-Fa-f]+),\s*0x([0-9A-Fa-f]+)\s*}')
                    m = r.search(line)
                    if m is not None:
                        self.erase= [m.group(1), m.group(2)]
                if "verification_block_start" in line:
                    self.verification_block_start = int(line.split('=')[1].replace("\"", ""),16)
                    # print(f"verification_block_start {self.verification_block_start}")
                if "verification_block_length" in line:
                    self.verification_block_length = int(line.split('=')[1].replace("\"", ""), 16)
                    # print(f"verification_block_length {self.verification_block_length}")
                if "sw_signature_dev" in line:
                    self.sw_signature_dev =bytearray.fromhex(line.split('=')[1].replace("\"", "").replace("0x", ""))
                    # print(f"sw_signature_dev {self.sw_signature_dev}")



            offset = binary_vbf.find(b"\n}")+2
            binary_data = binary_vbf[offset:]
            """
            StartAddress + Data  + Length + Data + CheckSum
            """
            while len(binary_data) > 0:
                start_address = int.from_bytes(binary_data[:4], 'big') #start
                length = int.from_bytes(binary_data[4:8], 'big') #size
                data = binary_data[8:8+length]
                checksum = binary_data[8+length:8+length+2]
                binary_data = binary_data[8+length+2:] #remain data
                vbf_block = VBF_Block(start_address.to_bytes(4,byteorder='big'),
                                             length.to_bytes(4,byteorder='big'),
                                             data,
                                             checksum
                                             )
                print("#"*20)
                print(vbf_block)
                self.blocks.append(vbf_block)

            print(time.time())
        except Exception:
            pass



    def get_header_attributes(self,attr):
        """
        an function to get the attributes in the header
        :param attr:
        :return:None if not exist or related value
        """
        attr_value = None
        for line in self.binary_header.split(b"\n"):
            line = re.sub(r'[\s;]', "", line.decode("utf-8"))
            if line.startswith("//"):
                continue
            if attr in line:
                attr_value = line.split('=')[1].replace("\"", "").replace("0x", "")
        print(f"{attr}： {attr_value}")

        return attr_value

if __name__ == "__main__":
    # with open('Application_Signed.vbf', "rb") as fd:
    #     datas = fd.read()
    Vtest = VBF("1.vbf")
    Vtest.get_header_attributes("sw_signature_dev")
    # print(Vtest.data[1])
    # print(Vtest.data_format_identifier)
    # print(Vtest.description)
    # print(Vtest.erase)
    # print(Vtest.file_checksum.hex())
    # print(Vtest.sw_signature_dev.hex())