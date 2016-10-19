#-*- coding:utf-8 -*-

import base64
import binascii
import struct

from Crypto.Cipher import Blowfish


CRYPTER_SALT = "H0w_many_r0ad_a_man_must_been_wa1k_d0wn, before_they_ca11_him_a_man."
BYTE_MAX_VALUE = 127


def int2bytes(v):
    l = 1
    bs = ["\x00"] * 8
    vv = v
    while vv >= 10:
        vv /= 10
        l += 1
    i = 1
    while i <= l:
        bs[l - i] = chr(v - v / 10 * 10 + 48)
        v = v / 10
        i += 1
    return bs


def bytes2int(bs):
    return int(binascii.hexlify(bs), 16)


def encodeVid(vid):
    '''
    convert video id to video code
    e.g. 132455291 => Bd8EpIzvW1E
    '''
    vid = int(vid)
    mode = Blowfish.MODE_CBC
    blow = Blowfish.new(CRYPTER_SALT[:32], mode, CRYPTER_SALT[32:40])

    # 将小于 100000000转换为 str(vid) + "\x00"格式 (共8位)
    # 将大于 100000000转换为 "\x12" (4位) + "\x7f"(4位)
    if(vid < 100000000):
        bs = int2bytes(vid)
    else:
        bs = ["\x00"] * 8
        bs[0] = ((vid >> 24) & 0xFF)
        bs[1] = ((vid >> 16) & 0xFF)
        bs[2] = ((vid >> 8) & 0xFF)
        bs[3] = ((vid) & 0xFF)
        bs[4] = BYTE_MAX_VALUE
        bs[5] = BYTE_MAX_VALUE
        bs[6] = BYTE_MAX_VALUE
        bs[7] = BYTE_MAX_VALUE
        bs = map(chr, bs)

    bs = "".join(bs)

    encrypt_bytes = blow.encrypt(bs)
    encode_chars = list(base64.b64encode(encrypt_bytes))

    for i in range(len(encode_chars)):
        if '=' == encode_chars[i]:
            break
        elif '+' == encode_chars[i]:
            encode_chars[i] = '-'
        elif '/' == encode_chars[i]:
            encode_chars[i] = '_'
    return "".join(encode_chars[:i])


def decodeVid(code):
    '''
    convert video code to video id
    e.g. Bd8EpIzvW1E => 132455291
    '''
    mode = Blowfish.MODE_CBC
    blow = Blowfish.new(CRYPTER_SALT[:32], mode, CRYPTER_SALT[32:40])
    code_list = list(code) 
    i = len(code)
    while i % 4 != 0:
        code_list.append("=")
        i += 1
    for i in xrange(0, len(code_list)):
        if code_list[i] == "-":
            code_list[i] = "+"
        elif code_list[i] == "_":
            code_list[i] = "/"
        else:
            pass
    source_bytes = base64.b64decode("".join(code_list))
    decrypt_bytes = blow.decrypt(source_bytes)
    if len(decrypt_bytes) == 8:
        last_char = struct.unpack("B", decrypt_bytes[7])
        if last_char and last_char[0] == BYTE_MAX_VALUE:
            a, b, c, d = struct.unpack("BBBB", decrypt_bytes[:4])
            return (a << 24) + (b << 16) + (c << 8) + d
        else:
            for i in xrange(0, len(decrypt_bytes)):
                i_char = struct.unpack("B", decrypt_bytes[i])
                if i_char and i_char[0] == 0:
                    break
            # 如果所有位均没有\x00的情况则将将整个字符串取整后返回
            else:
                i += 1
            return int("".join(decrypt_bytes[:i]))
    else:
        for i in xrange(0, len(decrypt_bytes)):
            i_char = struct.unpack("B", decrypt_bytes[i])
            if i_char and i_char[0] == 0:
                break
        else:
            i += 1
        return int("".join(decrypt_bytes[:i]))


if __name__ == '__main__':
    import requests
    resp = requests.get("http://www.tudou.com/crp/getAlbumItems.action?aid=115971&w=tudou_app")
    data = resp.json()
    data = data.get("data").get('items')
    for info in data:
        item_id = info.get("itemId")
        item_code = info.get("itemCode")
        print "test item_id: %s" % item_id
        if encodeVid(item_id) != item_code:
            print "error encode: %s" % item_id
        if decodeVid(item_code) != item_id:
            print "error decode: %s" % item_code





