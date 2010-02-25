from Crypto.Cipher import AES
import base64

def _lazysecret(secret, blocksize=32, padding='}'):
    """pads secret if not legal AES block size (16, 24, 32)"""
    if not len(secret) in (16, 24, 32):
        return secret + (blocksize - len(secret)) * padding

    return secret

def encrypt(plaintext, secret, lazy=True):
    """encrypt plaintext with secret
        plaintext   - content to encrypt
        secret      - secret to encrypt plaintext
        lazy        - pad secret if not legal blocksize (default: True)

        returns ciphertext (urlsafe base64 encoded)
    """
    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB)
    return base64.urlsafe_b64encode(encobj.encrypt(plaintext))

def decrypt(ciphertext, secret, lazy=True):
    """decrypt ciphertext with secret
        ciphertext  - encrypted content to decrypt (urlsafe base64 encoded)
        secret      - secret to decrypt ciphertext
        lazy        - pad secret if not legal blocksize (default: True)

        returns plaintext
    """
    secret = _lazysecret(secret) if lazy else secret
    encobj = AES.new(secret, AES.MODE_CFB)
    return encobj.decrypt(base64.urlsafe_b64decode(ciphertext))

