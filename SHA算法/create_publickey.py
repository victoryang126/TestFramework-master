from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization
from cryptography.x509 import load_pem_x509_certificate

def create_public_key_from_pem_string(pem_string):
    try:
        print(len(pem_string))
        pem_bytes = pem_string
        public_key = serialization.load_pem_public_key(
            pem_bytes,
            backend=default_backend())
        return public_key
    except Exception as e:
        print(f"Unable to load PEM file: {e}")
        return None

# 示例使用
pem_string = b'-----BEGIN PUBLIC KEY-----\nMIIBIjANBgkqhkiG9w0BAQEFAAOCAQ8AMIIBCgKCAQEAxBatyR4tPb+xIV3owCuN\ntDc2Cp/f8/sf7QunC3U7BHog3ksQl048kcIkS/hDUhXRZQQjFPtSd68xWihTgfcd\nR2ZARifcugDuQOBqdC2yiGHDinv+wNu8xfDx9W/n7EHjObvauTBLzVA15qMR936L\nYmcGmXhSeTQDFQB+IfPFBjQnaiJkS5RSBFChB1E3dxdNq7fDhnzc1V8ELV9Q6ZtY\nwvKn1LW+E8Z19Kg2e4gFnfRNd6u2ZJedys/4oJL2FYC7BeGR60rgKMIkCI+cnWGu\n+Wt6OZtiC9/i8BPZMjR8oMtVW7H+Zsk5Yp8DR95rF1n+jsVMQGRIdVkVbyZW2xJu\niQIDAQAB\n-----END PUBLIC KEY-----\n'

public_key = create_public_key_from_pem_string(pem_string)
if public_key:
    print(public_key)
    # print(public_key.)
else:
    print("Failed to load PEM file.")

def extract_rsa_public_key_info(public_key):
    # 获取 RSA 公钥的信息
    rsa_public_key = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    ).decode("utf-8")

    return rsa_public_key


def get_modulus_and_exponent(public_key):
    # 获取 RSA 公钥的 components
    components = public_key.public_numbers()

    # 获取 Modulus 和 Exponent
    modulus = components.n
    exponent = components.e

    return modulus, exponent
# public_key_info = extract_rsa_public_key_info(public_key)
# print(public_key_info)

modulus, exponent = get_modulus_and_exponent(public_key)
print("Modulus:", modulus)
print("Exponent:", exponent)