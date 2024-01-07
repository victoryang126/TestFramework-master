from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives.asymmetric import utils
import re, binascii, time, sys, os

def SignToSignatureDev(hash_input, hash_algorithm_input):
    with open(privateKey_pem, 'rb') as (privateKey_file):
        private_key = serialization.load_pem_private_key((privateKey_file.read()), password=b'0281922.')
    digest = binascii.a2b_hex(hash_input)
    salt_len = 0
    if hash_algorithm_input == 'SHA256':
        hash_algorithm_input = hashes.SHA256()
        salt_len = 32
    else:
        if hash_algorithm_input == 'SHA384':
            hash_algorithm_input = hashes.SHA384()
            salt_len = 48
        else:
            if hash_algorithm_input == 'SHA512':
                hash_algorithm_input = hashes.SHA512()
                salt_len = 64
    signature_out = private_key.sign(digest, padding.PSS(mgf=(padding.MGF1(hash_algorithm_input)),
      salt_length=salt_len), utils.Prehashed(hash_algorithm_input))
    signature_out = '0x' + '{:0^256}'.format(signature_out.hex().upper())
    return signature_out


def SignatureDevToVerify(hash_input, signature_input):
    with open('privateKey.pem', 'rb') as (privateKey_file):
        private_key = serialization.load_pem_private_key((privateKey_file.read()), password=None)
        public_key = private_key.public_key()
    digest = binascii.a2b_hex(hash_input)
    sig = binascii.a2b_hex(signature_input)
    try:
        public_key.verify(sig, digest, padding.PSS(mgf=(padding.MGF1(hashes.SHA256())),
          salt_length=32), utils.Prehashed(hashes.SHA256()))
    except Exception as e:
        try:
            print('Invalid Signature ', e)
        finally:
            e = None
            del e

    else:
        print('Verification OK.')


def ExtractInformation(identifier):
    if header_Dict.get(identifier):
        return header_Dict.get(identifier)
    print('Error: no ' + identifier + ' exist.')
    sys.exit()


if __name__ == '__main__':
    source_vbf = sys.argv[1]
    hash_algorithm = sys.argv[2]
    privateKey_pem = sys.argv[3]
    try:
        with open(source_vbf, 'rb') as (source_file):
            header_Dict = {}
            counter = 0
            while 1:
                line = source_file.readline()
                line = re.match(b'}', line) or line.decode()
                matchObj = re.match('(\\s*)(\\w+)(\\s*)=(\\s*)(\\S+)(\\s*);', line)
                if matchObj:
                    header_Dict[matchObj.group(2)] = matchObj.group(5)
                else:
                    matchObj = re.match('(.*){(\\W*)(\\w+)(\\W*)(\\w+)(\\W*)}', line)
                if matchObj:
                    header_Dict['erase' + str(counter)] = matchObj.group(3)
                    header_Dict['length' + str(counter)] = matchObj.group(5)
                    counter += 1
                else:
                    break

            counter = counter - 1
            identifierValue = ExtractInformation('verification_block_root_hash')
            root_hash = identifierValue[2:]
            signatureDev = SignToSignatureDev(root_hash, hash_algorithm)
            identifierValue = ExtractInformation('sw_part_number')
            matchObj = re.match('\\"(\\d*)\\"', identifierValue)
            if matchObj:
                sw_part_number = matchObj.group(1)
            identifierValue = ExtractInformation('sw_version')
            matchObj = re.match('\\"([A-Z])\\"', identifierValue)
            if matchObj:
                sw_version = matchObj.group(1)
            with open('VBFDevOut.vbf', 'wb') as (target_file):
                header_list = []
                header_list = [
                 'vbf_version = ' + header_Dict.get('vbf_version') + ';' + '\r\n',
                 'header {\r\n',
                 '       // Created by Geely VbfSign: ' + time.strftime('%Y-%m-%d %H:%M:%S', time.localtime(time.time())) + '\r\n',
                 '       sw_part_number = ' + header_Dict.get('sw_part_number') + ';' + '\r\n',
                 '       sw_version = ' + header_Dict.get('sw_version') + ';' + '\r\n',
                 '       sw_part_type = ' + header_Dict.get('sw_part_type') + ';' + '\r\n',
                 '       data_format_identifier = ' + header_Dict.get('data_format_identifier') + ';' + '\r\n',
                 '       ecu_address = ' + header_Dict.get('ecu_address') + ';' + '\r\n']
                if counter == 0:
                    header_list.extend([
                     '       erase = { { ' + header_Dict.get('erase' + str(counter)) + ', ' + header_Dict.get('length' + str(counter)) + ' } };' + '\r\n'])
                else:
                    if counter > 0:
                        flag = 0
                        while flag <= counter:
                            if flag == 0:
                                header_list.extend([
                                 '       erase = { { ' + header_Dict.get('erase' + str(flag)) + ', ' + header_Dict.get('length' + str(flag)) + ' },' + '\n'])
                            else:
                                if flag == counter - 1:
                                    header_list.extend([
                                     '                 { ' + header_Dict.get('erase' + str(flag)) + ', ' + header_Dict.get('length' + str(flag)) + ' }' + '\n'])
                                else:
                                    header_list.extend([
                                     '                 { ' + header_Dict.get('erase' + str(flag)) + ', ' + header_Dict.get('length' + str(flag)) + ' }' + '\n'])
                            flag += 1

                        header_list.extend(['               };\r\n'])
                    header_list.extend(['       verification_block_start = ' + header_Dict.get('verification_block_start') + ';' + '\r\n',
                     '       verification_block_length = ' + header_Dict.get('verification_block_length') + ';' + '\r\n',
                     '       verification_block_root_hash = ' + header_Dict.get('verification_block_root_hash') + ';' + '\r\n'])
                    header_list.extend(['       sw_signature_dev = ' + signatureDev + ';' + '\r\n'])
                    header_list.extend(['       file_checksum = ' + header_Dict.get('file_checksum') + ';' + '\r\n'])
                    header_list_encode = []
                    for lst in header_list:
                        header_list_encode.extend([lst.encode()])

                    target_file.writelines(header_list_encode)
                    target_file.write(line)
                    target_file.writelines(source_file.readlines())
                    print('OK')
        os.rename('VBFDevOut.vbf', sw_part_number + sw_version + '_dev.vbf')
    except Exception as result:
        try:
            print(result)
        finally:
            result = None
            del result