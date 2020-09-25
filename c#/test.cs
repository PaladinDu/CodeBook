/*
*@Auth PaladinDu
*@email wsdsc@qq.com
*@note Encrypts str in the specified character set
*/
using Newtonsoft.Json;
using System;
using System.Collections.Generic;
using System.Text;

namespace ConsoleApp2
{
    public class TestDataInfo
    {
        public string meta { get; set; }
        public string seed { get; set; }
        public List<List<string>> cases { get; set; }
    }
    class Program
    {
        static void TestData(CodeBook strCoding, byte[] key, byte[] data)
        {
            var encodeData = strCoding.Encryption(data, key);
            var decodeData = strCoding.Decryption(encodeData, key);
            if (Encoding.UTF8.GetString(data).Equals(Encoding.UTF8.GetString(decodeData)))
            {
                Console.WriteLine($"encryption success: {Encoding.UTF8.GetString(data)},{Encoding.UTF8.GetString(encodeData)}");
            }
            else
            {
                Console.WriteLine($"encryption error: {Encoding.UTF8.GetString(data)},{Encoding.UTF8.GetString(decodeData)}");
            }
        }
        static byte[] GetRandomBytes(byte[] validBytes, int len)
        {
            var ret = new byte[len];
            var rand = new Random();
            for (int i = 0; i < len; ++i)
            {
                ret[i] = validBytes[rand.Next(0, validBytes.Length)];
            }
            return ret;
        }
        static void TestRandomData(string testDataSavePath = null)
        {
            var chars = "abcdefghijklmnopqrstuvwxyz";
            chars += chars.ToUpper() + "0123456789`~!@#$%^&*()_+=-{}[]|:><,.\"'\\?/";
            var validCharBytes = Encoding.UTF8.GetBytes(chars);
            var codeBook = CodeBook.InitFromValidChars(validCharBytes);
            var codeBookMetaData = codeBook.GetMetaData();
            var codeBook2 = CodeBook.InitFromMetaData(codeBookMetaData);
            var seeds = new List<string> {
                "PaladinDu01",
                "PaladinDu02",
                "PaladinDu03",
            };
            var keys = new List<byte[]>();
            foreach (var seed in seeds)
            {
                keys.Add(codeBook.InitSeed(Encoding.UTF8.GetBytes(seed)));
            }
            var testDatas = new List<byte[]>
            {
                Encoding.UTF8.GetBytes("aaaaaaaaaaaaaaaaaaaaaaa"),
                Encoding.UTF8.GetBytes("aaaaaaaaaaaaaaaaaaaaaaab"),
                Encoding.UTF8.GetBytes("aaaaaaaaaaaaaaaaaaaaaaac"),
                Encoding.UTF8.GetBytes("aaaaaaaaaaaaaaaaaaaaaaad")
            };
            for (int i = 0; i < 1000; ++i)
            {
                testDatas.Add(GetRandomBytes(validCharBytes, 20));
            }
            foreach (var testData in testDatas)
            {
                TestData(codeBook, keys[0], testData);
                TestData(codeBook2, keys[0], testData);
            }
            foreach (var key in keys)
            {
                TestData(codeBook, key, testDatas[0]);
            }
            if (testDataSavePath != null)
            {
                var testCases = new List<List<string>>();
                foreach (var testData in testDatas)
                {
                    testCases.Add(new List<string> {
                        Encoding.UTF8.GetString(testData),
                        Encoding.UTF8.GetString(codeBook.Encryption(testData,keys[0]))
                    });
                }
                var json = JsonConvert.SerializeObject(new TestDataInfo
                {
                    meta = codeBookMetaData,
                    seed = seeds[0],
                    cases = testCases
                });
                System.IO.File.WriteAllText(testDataSavePath, json);
            }
        }
        static void TestByTestData(string testDataPath)
        {
            string text = System.IO.File.ReadAllText(testDataPath);
            var testDataInfo = JsonConvert.DeserializeObject<TestDataInfo>(text);
            var codeBook = CodeBook.InitFromMetaData(testDataInfo.meta);
            var key = codeBook.InitSeed(Encoding.UTF8.GetBytes(testDataInfo.seed));
            foreach (var caseData in testDataInfo.cases)
            {
                var decryptionData = codeBook.Decryption(Encoding.UTF8.GetBytes(caseData[1]), key);
                if (caseData[0].Equals(Encoding.UTF8.GetString(decryptionData)))
                {
                    Console.WriteLine($"decryption success:{caseData[0]},{caseData[1]}");
                }
                else
                {
                    Console.WriteLine($"decryption error:{caseData[0]},{caseData[1]},{Encoding.UTF8.GetString(decryptionData)}");
                }
            }
        }
        static void Main(string[] args)
        {
            var testDataPath = "e://cbtest.txt";
            TestByTestData(testDataPath);
            TestRandomData(testDataPath);
            TestByTestData(testDataPath);
        }
    }
}