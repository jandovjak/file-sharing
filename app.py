from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Util.Padding import pad, unpad
import secrets

BLOCK_SIZE = 16


def generate_iv() -> bytes:
    return secrets.token_bytes(BLOCK_SIZE)


def hash_password(password: str) -> bytes:
    hash_object = SHA3_256.new()
    password_bytes = bytearray(password.encode('utf-8'))
    hash_object.update(password_bytes)
    return bytes(hash_object.digest())


def encrypt_with_iv(plaintext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return cipher.encrypt(pad(plaintext, BLOCK_SIZE))


def encrypt(plaintext: bytes, key: bytes) -> bytes:
    iv = generate_iv()
    return iv + encrypt_with_iv(plaintext, key, iv)


def decrypt_with_iv(ciphertext: bytes, key: bytes, iv: bytes) -> bytes:
    cipher = AES.new(key, AES.MODE_CBC, iv)
    return unpad(cipher.decrypt(ciphertext), BLOCK_SIZE)


def decrypt(ciphertext: bytes, key: bytes) -> bytes:
    iv = ciphertext[:BLOCK_SIZE]
    return decrypt_with_iv(ciphertext[BLOCK_SIZE:], key, iv)


def encrypt_file(input_file: str, output_file: str, key: bytes) -> None:
    with open(input_file, 'rb') as f:
        plaintext = f.read()
    ciphertext = encrypt(plaintext, key)
    with open(output_file, 'wb') as f:
        f.write(ciphertext)


def decrypt_file(input_file: str, output_file: str, key: bytes) -> None:
    with open(input_file, 'rb') as f:
        ciphertext = f.read()
    plaintext = decrypt(ciphertext, key)
    with open(output_file, 'wb') as f:
        f.write(plaintext)


if __name__ == '__main__':
    key = hash_password('MySuperSecretPassword123!')
    encrypt_file('files/example.txt', 'files/example.bin', key)
    decrypt_file('files/example.bin', 'files/example2.txt', key)
    decrypt_file('files/5cd994a7-c9a6-442a-a3b6-be1e2a9955ef',
                 'files/example_decrypted.txt', key)
