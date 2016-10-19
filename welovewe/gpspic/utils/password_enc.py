import base64
from Crypto.Cipher import AES
from conf import settings

_cipher = AES.new(settings.AES_KEY)

# for login password
def decode_password(e, pc):
    raw = _cipher.decrypt(base64.b64decode(e))
    return raw[:len(raw) - pc]

# for cookie encrypt
def _pad(s):
    BS = len(settings.AES_KEY)
    return s + (BS - len(s) % BS) * chr(BS - len(s) % BS)

def encrypt(text):
    data = _pad(text)
    return _cipher.encrypt(data).encode('hex')

# for play url encrypt
def _pad1(s):
    BS = len(settings.AES_KEY)
    return s + (BS - len(s) % BS) * settings.AES_PADDING

def encrypt_base64(text):
    data = _pad1(text)
    return base64.b64encode(_cipher.encrypt(data))

