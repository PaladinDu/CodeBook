"""
@Auth PaladinDu
@email wsdsc@qq.com
@note Encrypts str in the specified character set
"""
from code_book import *
import time
import json


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


if __name__ == "__main__":
    test_data_save_path= "e://cbtest.txt"
    test_by_test_data(test_data_save_path)
    test_random_data(test_data_save_path)
    test_by_test_data(test_data_save_path)