from Crypto.Cipher import AES
from hashlib import sha1

class CheckSumError(Exception):
    pass

def _lazysecret(secret, blocksize=32, padding='}'):
    """pads secret if not legal AES block size (16, 24, 32)"""
    if not len(secret) in (16, 24, 32):
        return secret + (blocksize - len(secret)) * padding

    return secret

def encrypt(plaintext, secret, lazy=True, checksum=True):
    """encrypt plaintext with secret
        plaintext   - content to encrypt
        secret      - secret to encrypt plaintext
        lazy        - pad secret if less than legal blocksize (default: True)
        checksum    - attach sha1 digest byte encoded (default: True)

        returns ciphertext
    """
    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB)
    if checksum:
        plaintext += sha1(plaintext).digest()

    return encobj.encrypt(plaintext)

def decrypt(ciphertext, secret, lazy=True, checksum=True):
    """decrypt ciphertext with secret
        ciphertext  - encrypted content to decrypt
        secret      - secret to decrypt ciphertext
        lazy        - pad secret if less than legal blocksize (default: True)
        checksum    - verify sha1 digest byte encoded checksum (default: True)

        returns plaintext
    """
    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB)
    plaintext = encobj.decrypt(ciphertext)
    if checksum:
        digest, plaintext = (plaintext[-20:], plaintext[:-20])
        if not digest == sha1(plaintext).digest():
            raise CheckSumError("checksum mismatch")

    return plaintext

