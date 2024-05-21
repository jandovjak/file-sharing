from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Util.Padding import pad, unpad
from Crypto.Random import get_random_bytes


BLOCK_SIZE = 16


def hash_password(password: str) -> bytearray:
    hash_object = SHA3_256.new()
    password_bytes = bytearray(password.encode('utf-8'))
    hash_object.update(password_bytes)
    return bytearray(hash_object.digest())


def encrypt(plaintext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(plaintext, BLOCK_SIZE))


def decrypt(ciphertext, key, iv):
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)


def encrypt_file(input_file, output_file, key, iv):
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    ciphertext = encrypt(plaintext, key, iv)
    with open(output_file, 'wb') as f:
        f.write(ciphertext)


def decrypt_file(input_file, output_file, key, iv):
    with open(input_file, 'rb') as f:
        ciphertext = f.read()
    plaintext = decrypt(ciphertext, key, iv)
    with open(output_file, 'wb') as f:
        f.write(plaintext)


if __name__ == '__main__':
    key = hash_password('aaaa')
    iv = bytes([0] * 16)
    encrypt_file('files/example.txt', 'files/example.bin', key, iv)
    decrypt_file('files/example.bin', 'files/example2.txt', key, iv)
