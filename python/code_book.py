"""
@Auth PaladinDu
@email wsdsc@qq.com
@note Encrypts str in the specified character set
"""
import random


class CodeBook:
    MIN_KEY_LEN = 512
    INVALID_INDEX = -1
    HEX_TO_NUM_MAP = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 1, 2, 3, 4, 5, 6, 7, 8, 9, 0, 0, 0, 0, 0, 0,
                        0, 10, 11, 12, 13, 14, 15, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 10, 11, 12, 13, 14, 15, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
                        0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
    NUM_TO_HEX_MAP = b"0123456789ABCDEF"

    def __init__(self):
        self.char_to_index_map = None
        self.index_to_char_map = None
        self.encryption_map = None
        self.decryption_map = None
        self.chars_count = 0

    @staticmethod
    def init_from_valid_chars(valid_chars_bytes):
        ret = CodeBook()
        char_map = [CodeBook.INVALID_INDEX for _ in range(256)]
        ret.char_to_index_map = [CodeBook.INVALID_INDEX for _ in range(256)]
        ret.index_to_char_map = [CodeBook.INVALID_INDEX for _ in range(256)]
        char_count = 0
        for char in valid_chars_bytes:
            char_map[char] = 1
        for i in range(256):
            if char_map[i] == 1:
                ret.char_to_index_map[i] = char_count
                ret.index_to_char_map[char_count] = i
                char_count += 1
        ret.chars_count = char_count
        ret.index_to_char_map = ret.index_to_char_map[:char_count]
        ret.encryption_map = [i for i in range(char_count)]
        ret.decryption_map = [0 for _ in range(char_count)]
        for i in range(char_count):
            rand = random.randint(0, char_count - i - 1)
            tmp_code = ret.encryption_map[i]
            ret.encryption_map[i] = ret.encryption_map[i+rand]
            ret.encryption_map[i + rand] = tmp_code
            ret.decryption_map[ret.encryption_map[i]] = i
        return ret

    @staticmethod
    def init_from_meta_data(meta_data_bytes):
        ret = CodeBook()
        ret.chars_count = len(meta_data_bytes) // 4
        ret.char_to_index_map = [0]*256
        ret.index_to_char_map = [0]*ret.chars_count
        ret.encryption_map = [0]*ret.chars_count
        ret.decryption_map = [0]*ret.chars_count
        valid_chars_meta = meta_data_bytes[:ret.chars_count * 2]
        char_change_meta = meta_data_bytes[ret.chars_count * 2:]
        for i in range(ret.chars_count):
            tmp_char = ((CodeBook.HEX_TO_NUM_MAP[valid_chars_meta[i * 2]] << 4) | CodeBook.HEX_TO_NUM_MAP[valid_chars_meta[i * 2 + 1]])
            ret.char_to_index_map[tmp_char] = i
            ret.index_to_char_map[i] = tmp_char
            tmp_char = ((CodeBook.HEX_TO_NUM_MAP[char_change_meta[i * 2]] << 4) | CodeBook.HEX_TO_NUM_MAP[char_change_meta[i * 2 + 1]])
            ret.encryption_map[i] = tmp_char
            ret.decryption_map[tmp_char] = i
        return ret

    def get_valid_chars(self):
        return self.index_to_char_map

    def get_mate_data(self):
        meta_data = bytearray(self.chars_count*4)
        for i in range(self.chars_count):
            meta_data[i * 2] = CodeBook.NUM_TO_HEX_MAP[self.index_to_char_map[i] >> 4]
            meta_data[i * 2 + 1] = CodeBook.NUM_TO_HEX_MAP[self.index_to_char_map[i] & 0x0f]
            meta_data[i * 2 + self.chars_count*2] = CodeBook.NUM_TO_HEX_MAP[self.encryption_map[i] >> 4]
            meta_data[i * 2 + 1 + self.chars_count*2] = CodeBook.NUM_TO_HEX_MAP[self.encryption_map[i] & 0x0f]
        return bytes(meta_data)

    def init_seed(self, seed_bytes):
        if len(seed_bytes) < CodeBook.MIN_KEY_LEN:
            seed_bytes = seed_bytes + b'\0' * (CodeBook.MIN_KEY_LEN - len(seed_bytes))
        key_bytearray = bytearray(seed_bytes)
        char_key = 0
        for i in range(len(key_bytearray)):
            char_key = (char_key + key_bytearray[i] + i) % self.chars_count
            key_bytearray[i] = self._enchange(key_bytearray[i], char_key)
        for i in range(len(key_bytearray)):
            key_bytearray[i] = self._enchange(key_bytearray[i], char_key)
            char_key = (char_key + key_bytearray[i] + i) % self.chars_count
        return bytes(key_bytearray)

    def _data_to_index(self, data_bytearray):
        for i in range(len(data_bytearray)):
            data_bytearray[i] = self.char_to_index_map[data_bytearray[i]]

    def _index_to_data(self, index_bytearray):
        for i in range(len(index_bytearray)):
            index_bytearray[i] = self.index_to_char_map[index_bytearray[i]]

    def _enchange(self, data, key):
        return self.encryption_map[(data + key) % self.chars_count]

    def _dechange(self, data, key):
        return (self.decryption_map[data] + self.chars_count - key % self.chars_count) % self.chars_count

    def _encryption(self, data_bytearray, key_bytes):
        for i in range(len(key_bytes)):
            data_index = i % len(data_bytearray)
            data_bytearray[data_index] = self._enchange(data_bytearray[data_index], key_bytes[i])
        j = 0
        char_key = key_bytes[j]
        for i in range(len(data_bytearray)):
            data_bytearray[i] = self._enchange(data_bytearray[i], char_key)
            j += 1
            if j >= len(key_bytes):
                j = 0
            char_key = (key_bytes[j] + data_bytearray[i]) % self.chars_count
        char_key = key_bytes[j]
        for i in range(len(data_bytearray), 0, -1):
            i -= 1
            data_bytearray[i] = self._enchange(data_bytearray[i], char_key)
            j += 1
            if j >= len(key_bytes):
                j = 0
            char_key = (key_bytes[j] + data_bytearray[i]) % self.chars_count

    def _decryption(self, data_bytearray, key_bytes):
        j = (len(data_bytearray)*2-1) % len(key_bytes)
        for i in range(len(data_bytearray)):
            tmp_char_seed = 0
            if i < len(data_bytearray) - 1:
                tmp_char_seed = data_bytearray[i + 1]
            char_key = (key_bytes[j] + tmp_char_seed) % self.chars_count
            data_bytearray[i] = self._dechange(data_bytearray[i], char_key)
            if j == 0:
                j = len(key_bytes) - 1
            else:
                j -= 1

        for i in range(len(data_bytearray), 0, -1):
            i = i - 1
            tmp_char_seed = 0
            if i > 0:
                tmp_char_seed = data_bytearray[i - 1]
            char_key = (key_bytes[j] + tmp_char_seed) % self.chars_count
            data_bytearray[i] = self._dechange(data_bytearray[i], char_key)
            if j == 0:
                j = len(key_bytes) - 1
            else:
                j -= 1
        for i in range(len(key_bytes)):
            i = len(key_bytes) - i -1
            data_index = i % len(data_bytearray)
            data_bytearray[data_index] = self._dechange(data_bytearray[data_index], key_bytes[i])

    def encryption(self, origin_data, key_bytes):
        data_bytearray = bytearray(origin_data)
        self._data_to_index(data_bytearray)
        self._encryption(data_bytearray, key_bytes)
        self._index_to_data(data_bytearray)
        return bytes(data_bytearray)

    def decryption(self, encryption_data, key_bytes):
        data_bytearray = bytearray(encryption_data)
        self._data_to_index(data_bytearray)
        self._decryption(data_bytearray, key_bytes)
        self._index_to_data(data_bytearray)
        return bytes(data_bytearray)





