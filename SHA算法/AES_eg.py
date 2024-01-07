from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import cmac
from cryptography.hazmat.primitives.padding import PKCS7
import os

def pad(data):
    # PKCS7 Padding
    block_size = 16
    padding_length = block_size - len(data) % block_size
    padding = bytes([padding_length] * padding_length)
    return data + padding

def unpad(data):
    # PKCS7 Unpadding
    padding_length = data[-1]
    return data[:-padding_length]

def encrypt_aes(key, plaintext):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    encryptor = cipher.encryptor()
    ciphertext = encryptor.update(pad(plaintext)) + encryptor.finalize()
    return ciphertext

def decrypt_aes(key, ciphertext):
    cipher = Cipher(algorithms.AES(key), modes.ECB(), backend=default_backend())
    decryptor = cipher.decryptor()
    plaintext = unpad(decryptor.update(ciphertext) + decryptor.finalize())
    return plaintext

def generate_aes_cmac(key, data):
    cmac_algorithm = cmac.CMAC(algorithms.AES(key), backend=default_backend())
    cmac_algorithm.update(data)
    return cmac_algorithm.finalize()

# 128-bit AES key (16 bytes)
aes_key = os.urandom(16)

# Example usage of AES encryption and decryption
plaintext_message = b"Hello, AES!"
encrypted_message = encrypt_aes(aes_key, plaintext_message)
decrypted_message = decrypt_aes(aes_key, encrypted_message)

print("Original Message:", plaintext_message)
print("Encrypted Message:", encrypted_message)
print("Decrypted Message:", decrypted_message)

# Example usage of AES-CMAC
data_to_mac = b"Data to be MACed"
mac = generate_aes_cmac(aes_key, data_to_mac)

print("AES-CMAC:", mac.hex())
