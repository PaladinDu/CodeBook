/*
*@Auth PaladinDu
*@email wsdsc@qq.com
*@note Encrypts str in the specified character set
*/
using System;
using System.Text;


public class CodeBook
{

    static byte[] HexToNumMap = new byte[256] { 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0,
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
                                                0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0};
    static byte[] NumToHexMap = Encoding.UTF8.GetBytes("0123456789ABCDEF");
    const int MIN_KEY_LEN = 512;
    const int InvalidIndex = -1;
    private int[] CharToIndexMap { get; set; }
    private byte[] IndexToCharMap { get; set; }
    private byte[] EncryptionMap { get; set; }
    private byte[] DecryptionMap { get; set; }
    private int CharsCount { get; set; }
    public CodeBook()
    {

    }
    static public CodeBook InitFromValidChars(byte[] validChars)
    {
        var ret = new CodeBook();
        ret.CharToIndexMap = new int[256];
        ret.CharsCount = validChars.Length;
        var charCount = 0;
        var charMap = new int[256];
        for (int i = 0; i < 256; ++i)
        {
            charMap[i] = InvalidIndex;
        }
        foreach (var validChar in validChars)
        {
            if (charMap[validChar] != 1)
            {
                charMap[validChar] = 1;

                charCount += 1;
            }
        }
        ret.IndexToCharMap = new byte[charCount];
        for (int i = 0, j = 0; i < 256; ++i)
        {
            if (charMap[i] == 1)
            {
                ret.IndexToCharMap[j] = (byte)i;
                ret.CharToIndexMap[i] = j;
                j++;
            }
        }
        ret.EncryptionMap = new byte[charCount];
        ret.DecryptionMap = new byte[charCount];
        for (int i = 0; i < ret.CharsCount; ++i)
        {
            ret.EncryptionMap[i] = (byte)i;
        }
        var rand = new Random();
        for (int i = 0; i < ret.CharsCount; ++i)
        {
            var randInt = rand.Next(0, ret.CharsCount - i);
            var tmpCode = ret.EncryptionMap[i];
            ret.EncryptionMap[i] = ret.EncryptionMap[i + randInt];
            ret.DecryptionMap[ret.EncryptionMap[i]] = (byte)i;
            ret.EncryptionMap[i + randInt] = tmpCode;
        }
        return ret;
    }
    static public CodeBook InitFromMetaData(string metaData)
    {
        var ret = new CodeBook();
        byte[] metaDataBytes = Encoding.UTF8.GetBytes(metaData);
        ret.CharsCount = metaData.Length/4;
        ret.CharToIndexMap = new int[256];
        ret.IndexToCharMap = new byte[ret.CharsCount];
        ret.EncryptionMap = new byte[ret.CharsCount];
        ret.DecryptionMap = new byte[ret.CharsCount];
        for (int i = 0; i < ret.CharsCount; ++i)
        {
            var tmpChar = (byte)((HexToNumMap[metaDataBytes[i * 2]] << 4) | HexToNumMap[metaDataBytes[i * 2 + 1]]);
            ret.CharToIndexMap[tmpChar] = i;
            ret.IndexToCharMap[i] = tmpChar;
            tmpChar = (byte)((HexToNumMap[metaDataBytes[i * 2 + ret.CharsCount * 2]] << 4) | HexToNumMap[metaDataBytes[i * 2 + 1 + ret.CharsCount * 2]]);
            ret.EncryptionMap[i] = tmpChar;
            ret.DecryptionMap[tmpChar] = (byte)i;
        }
        return ret;
    }

    public byte[] GetValidChars()
    {
        return this.IndexToCharMap;
    }
    public string GetMetaData()
    {
        byte[] metaData = new byte[this.CharsCount * 4];
        for (int i = 0; i < this.CharsCount; ++i)
        {
            metaData[i * 2] = CodeBook.NumToHexMap[this.IndexToCharMap[i] >> 4]; ;
            metaData[i * 2 + 1] = CodeBook.NumToHexMap[this.IndexToCharMap[i] & 0x0f];
            metaData[i * 2 + this.CharsCount * 2] = CodeBook.NumToHexMap[this.EncryptionMap[i] >> 4];
            metaData[i * 2 + 1 + this.CharsCount * 2] = CodeBook.NumToHexMap[this.EncryptionMap[i] & 0x0f];
        }
        return Encoding.UTF8.GetString(metaData);
    }
    public byte[] InitSeed(byte[] seed)
    {
        byte[] key;
        if (seed.Length < MIN_KEY_LEN)
        {
            key = new byte[MIN_KEY_LEN];
            for (int i = seed.Length; i < MIN_KEY_LEN; ++i)
            {
                key[i] = 0;
            }
        }
        else
        {
            key = new byte[seed.Length];
        }

        Array.Copy(seed, key, seed.Length);
        int charKey = 0;
        for (int i = 0; i < key.Length; ++i)
        {
            charKey = (charKey + key[i] + i) % this.CharsCount;
            key[i] = this.enchange(key[i], (byte)charKey);
        }
        for (int i = 0; i < key.Length; ++i)
        {
            key[i] = this.enchange(key[i], (byte)charKey);
            charKey = (charKey + key[i] + i) % this.CharsCount;
        }
        return key;
    }
    private byte enchange(byte num, byte key)
    {
        return this.EncryptionMap[(num + key) % this.CharsCount];
    }
    private byte dechange(byte num, byte key)
    {
        return (byte)((this.DecryptionMap[num] + this.CharsCount - key % this.CharsCount) % this.CharsCount);
    }
    private void dataToIndex(byte[] data)
    {
        for (int i = 0; i < data.Length; ++i)
        {
            data[i] = (byte)this.CharToIndexMap[data[i]];
        }
    }
    private void indexToData(byte[] data)
    {
        for (int i = 0; i < data.Length; ++i)
        {
            data[i] = this.IndexToCharMap[data[i]];
        }
    }
    private void encryption(byte[] data, byte[] key)
    {
        for (int i = 0; i < key.Length; ++i)
        {
            data[i % data.Length] = this.enchange(data[i % data.Length], key[i]);
        }

        var j = 0;
        int charKey = key[j];
        for (int i = 0; i < data.Length; ++i)
        {
            data[i] = this.enchange(data[i], (byte)charKey);
            j++;
            if (j >= key.Length)
            {
                j = 0;
            }
            charKey = (key[j] + data[i]) % this.CharsCount;
        }
        charKey = key[j];
        for (int i = data.Length - 1; i >= 0; --i)
        {
            data[i] = this.enchange(data[i], (byte)charKey);
            j++;
            if (j >= key.Length)
            {
                j = 0;
            }
            charKey = (key[j] + data[i]) % this.CharsCount;
        }
    }
    private void decryption(byte[] data, byte[] key)
    {
        var j = (data.Length * 2 - 1) % key.Length;
        for (int i = 0; i < data.Length; ++i)
        {
            var charKey = 0;
            if (i < data.Length - 1)
            {
                charKey = data[i + 1];
            }
            charKey = (key[j] + charKey) % this.CharsCount;
            data[i] = this.dechange(data[i], (byte)charKey);
            if (j == 0)
            {
                j = key.Length - 1;
            }
            else
            {
                --j;
            }
        }
        for (int i = data.Length - 1; i >= 0; --i)
        {
            var charSeed = 0;
            if (i > 0)
            {
                charSeed = data[i - 1];
            }
            charSeed = (key[j] + charSeed) % this.CharsCount;
            data[i] = this.dechange(data[i], (byte)charSeed);
            if (j == 0)
            {
                j = key.Length - 1;
            }
            else
            {
                --j;
            }
        }

        for (int i = key.Length - 1; i >= 0; --i)
        {
            data[i % data.Length] = this.dechange(data[i % data.Length], key[i]);
        }
    }
    public byte[] Encryption(byte[] data, byte[] key)
    {
        if (data == null || data.Length == 0 || key == null || key.Length == 0)
        {
            throw new Exception("Invalid param");
        }
        var ret = new byte[data.Length];
        Array.Copy(data, ret, data.Length);
        this.dataToIndex(ret);
        this.encryption(ret, key);
        this.indexToData(ret);
        return ret;
    }
    public byte[] Decryption(byte[] data, byte[] key)
    {
        if (data == null || data.Length == 0 || key == null || key.Length == 0)
        {
            throw new Exception("Invalid param");
        }
        var ret = new byte[data.Length];
        Array.Copy(data, ret, data.Length);
        this.dataToIndex(ret);
        this.decryption(ret, key);
        this.indexToData(ret);
        return ret;
    }
}
