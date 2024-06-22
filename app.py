from Crypto.Cipher import AES
from Crypto.Hash import SHA3_256
from Crypto.Util.Padding import pad, unpad
import secrets
import argparse
import getpass

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


def get_password() -> str:
    return getpass.getpass(prompt='Password: ')


def main():
    parser = argparse.ArgumentParser(
                    prog='ProgramName',
                    description='What the program does',
                    epilog='Text at the bottom of help')
    parser.add_argument('-i', '--input_file', type=str, required=True,
                        help="Path to the input file")
    parser.add_argument('-o', '--output_file', type=str, required=True,
                        help="Path to the output file")
    parser.add_argument('-e', '--encrypt', action='store_true',
                        help="Encrypt the input file to the output file")
    parser.add_argument('-d', '--decrypt', action='store_true',
                        help="Decrypt the input file to the output file")
    parser.add_argument('-p', '--password', type=str,
                        help="Password given as an argument. If not given, user will be asked in session.")
    parser.add_argument('-v', '--verbose', action='store_true',
                        help="Verbose mode")
    args = parser.parse_args()

    # Predicate
    if (not args.encrypt and not args.decrypt) or\
       (args.encrypt and args.decrypt):
        parser.error("Encryption (-e) XOR decryption (-d) argument is required")
    if not args.password:
        args.password = get_password()
    key = hash_password(args.password)
    if args.encrypt:
        encrypt_file(args.input_file, args.output_file, key)
    if args.decrypt:
        decrypt_file(args.input_file, args.output_file, key)


if __name__ == '__main__':
    main()
