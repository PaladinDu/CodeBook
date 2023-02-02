"""
@Auth PaladinDu
@email wsdsc@qq.com
@note Encrypts str in the specified character set
"""
from code_book import *
import time
import json
import binascii

def test(test_code_book, test_key_bytes, test_data_bytes):
    encode_data = test_code_book.encryption(test_data_bytes, test_key_bytes)
    decode_data = test_code_book.decryption(encode_data, test_key_bytes)
    if test_data_bytes != decode_data:
        print("encryption error:", test_data_bytes, decode_data)
    else:
        print("encryption success:", test_data_bytes, encode_data)


def test_random_data(test_data_save_path=None):
    chars = "abcdefghijklmnopqrstuvwxyz"
    chars = chars + chars.upper() + """0123456789`~!@#$%^&*()_+=-{}[]|:><,."'\\?/"""
    code_book = CodeBook.init_from_valid_chars(chars.encode("utf8"))
    code_bool_meta_data = code_book.get_mate_data()

    print(code_bool_meta_data, len(code_bool_meta_data))
    code_book2 = CodeBook.init_from_meta_data(code_bool_meta_data)
    seeds = ["PaladinDu{}".format(int(time.time()) + i) for i in range(10)]
    key_bytes = [code_book.init_seed(key.encode("utf8")) for key in seeds]
    test_datas = [
        b"aaaaaaaaaaaaaaaaaaaaaaa",
        b"aaaaaaaaaaaaaaaaaaaaaaab",
        b"aaaaaaaaaaaaaaaaaaaaaaac",
        b"aaaaaaaaaaaaaaaaaaaaaaad"
    ]
    test_datas += ["{}".format(i).encode("utf8") for i in range(1000)]
    for test_data in test_datas:
        test(code_book, key_bytes[0], test_data)
        test(code_book2, key_bytes[0], test_data)
    for key_bytearray in key_bytes:
        test(code_book, key_bytearray, test_datas[0])
    test_data1 = test_datas[0]
    for i in range(256):
        encode_data = code_book.encryption(test_data1, key_bytearray)
        print(encode_data)
        test_data1 = encode_data
    if test_data_save_path != None:
        fw = open(test_data_save_path, "w")
        fw.write(json.dumps({
            "meta": code_bool_meta_data.decode("utf8"),
            "seed": seeds[0],
            "cases": [[test_data.decode("utf8"), code_book.encryption(test_data, key_bytes[0]).decode("utf8")] for
                      test_data in test_datas]
        }))
        fw.close()


def test_by_test_data(test_data_path):
    test_data_info = json.load(open(test_data_path))
    code_book = CodeBook.init_from_meta_data(test_data_info["meta"].encode("utf8"))
    seed = test_data_info["seed"]
    key = code_book.init_seed(seed.encode("utf8"))
    for origin_data, encryption_data in test_data_info["cases"]:
        if code_book.decryption(encryption_data.encode("utf8"), key) == origin_data.encode("utf8"):
            print("decryption success", origin_data, encryption_data)
        else:
            print("decryption error", origin_data, encryption_data,
                  code_book.decryption(encryption_data.encode("utf8"), key).decode("utf8"))


def get_code_by_incr(codebook:CodeBook,num):
    count = len("abcdefghijklmnopqrstuvcxyz1234567890")
    tmp = bytearray("12345678".encode("utf8"))
    tmp_c = 0
    tmp_c2 = 0
    for i in range(8):
        tmp_c3 = tmp_c2
        tmp_c2 = tmp_c
        tmp_c = (num+tmp_c+tmp_c3) % count
        tmp[i] = tmp_c

        tmp[i] = codebook.index_to_char_map[tmp[i]]
        num = num//count
    ret = bytes(tmp)
    return ret

meta = "303132333435363738394142434445464748494A4B4C4D4E4F505152535455565758595A6162636465666768696A6B6C6D6E6F707172737475767778797A0E0A33142D0628313A03043D071B38240D1A343205162739150810301E211F2935220F25002A2B010C1D1C2E02113B2337133C2F0B191809122C17202636"
code_book = CodeBook.init_from_meta_data(meta.encode("utf8"))
key = code_book.init_seed("coconut".encode("utf8"))

def hex_to_str(str):
    hex = str.encode('utf-8')
    str_bin = binascii.unhexlify(hex)
    return str_bin.decode('utf-8')

def str_to_hex(str):
    str_bin = str.encode('utf-8')
    return binascii.hexlify(str_bin).decode('utf-8')

def encode_text(str):
    hex_str = str_to_hex(str)
    return code_book.encryption(hex_str.encode("utf8"), key).decode("utf8")

def decode_text(str):
    origin_str = code_book.decryption(str.encode("utf8"), key).decode("utf8")
    return hex_to_str(origin_str)

if __name__ == "__main__":
    str = "sb4m8Y5TvludGCbmvdIxCdVJJbCeedkUbSY0AebJiGWFS9kk63V9V4CGyp9jx8P5G7l6OxVgi4qsmeKUTZX9vtM21bPkOYQdKLcmX7kiYdZnu7U005k5d2Gqof3vt4A4yCq4iRt8dambByBMfSAS4ln22Z6INZBgT7WxANisAFGXa19RAiPaJDJKyUS1FUSxp4pl0W30oZ2dGXnIjlQzsTnL6KQviaBt7vZFX6PouNyDpsGEdVdQANJ4EuflR6M1i1EVuPCKacXIEMzlkedXRGhg1uzgN9YYJJppAP8sK5GVLkkWikf1vGbuIdvsKbuBGnyJNoMvQygoCAHb2fylOwrbn6UoUioOivEQg5cjmge5skWBd0QusdBUhF"
    print(decode_text(str))