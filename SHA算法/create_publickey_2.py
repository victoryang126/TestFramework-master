from cryptography.hazmat.primitives.serialization import load_pem_public_key
from cryptography.hazmat.primitives import serialization
from cryptography.hazmat.primitives.asymmetric import padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend

def load_public_key(pem_file_path):
    with open(pem_file_path, 'rb') as pem_file:
        pem_data = pem_file.read()
        public_key = load_pem_public_key(pem_data, backend=default_backend())
    return public_key

def pem_to_der(public_key):
    der_data = public_key.public_bytes(
        encoding=serialization.Encoding.DER,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    return der_data

def encrypt_with_public_key(public_key, plain_text):
    cipher_text = public_key.encrypt(
        plain_text,
        padding.OAEP(
            mgf=padding.MGF1(algorithm=hashes.SHA256()),
            algorithm=hashes.SHA256(),
            label=None
        )
    )
    return cipher_text

# 加载PEM格式的公钥
public_key = load_public_key("publickey_pem")

# 转换为DER编码
der_data = pem_to_der(public_key)