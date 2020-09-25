/*
*@Auth PaladinDu
*@email wsdsc@qq.com
*@note Encrypts str in the specified character set
*/
#include <stdio.h>
#include "CodeBook.h"

void main() {
	const unsigned char* validChars = (const unsigned char*)"abcdefghijklmnopqrstuvwxyzABCDEFGHIJKLMNOPQRSTUVWXYZ0123456789~`!@#$%^&*()_+-=|}{[]\\:\"\';<>?/., ";
	int validCharsLen = 95;
	const unsigned char* seed = (const unsigned char*)"PaladinDu2020";
	int seedLen = 13;
	unsigned char key[513];
	int keyLen = 0;
	key[512] = '\0';
	CodeBook* pCodeBook = CodeBook::RandomInitByValidChars(validChars, validCharsLen);
	char metaData[2048];
	int metaDataLen = 0;
	pCodeBook->GetMateData(metaData, &metaDataLen);
	CodeBook* pCodeBook2 = CodeBook::InitFromMetaData(metaData, metaDataLen);
	pCodeBook->InitSeed(seed, seedLen, key, &keyLen);
	unsigned char testData[2049];
	int testDataLen = 10;
	testData[testDataLen] = '\0';

	for (int j = 0; j < 100; ++j) {
		

		for (int i = 0; i < testDataLen; ++i) {
			testData[i] = validChars[(i *j* 1001) % validCharsLen];
		}
		printf("Test time:%02d:\n", j);
		printf("testData1:%s\n", testData);
		pCodeBook->Encryption(testData, testDataLen, key, keyLen);
		printf("encrData1:%s\n", testData);
		pCodeBook->Decryption(testData, testDataLen, key, keyLen);
		printf("decrData1:%s\n", testData);
		pCodeBook2->Encryption(testData, testDataLen, key, keyLen);
		printf("encrData2:%s\n", testData);
		pCodeBook2->Decryption(testData, testDataLen, key, keyLen);
		printf("decrData2:%s\n", testData);
		printf("\n");
	}
	//
	const char* otherCodeBookMeta = "2122232425262728292A2B2C2D2E2F303132333435363738393A3C3D3E3F404142434445464748494A4B4C4D4E4F505152535455565758595A5B5C5D5E5F606162636465666768696A6B6C6D6E6F707172737475767778797A7B7C7D7E581B452C4216055C231F0A31361C113A523032150714482051123D0E1E0D2A471710541D0B282506500C5322353F553B4C41191A262D4359565A46374B3427094A21012F29383C0233443E4E39245B4D1340044F180F0003082B49572E";
	int otherCodeBookLen = 372;
	CodeBook* pCodeBook3 = CodeBook::InitFromMetaData(otherCodeBookMeta, otherCodeBookLen);
	const unsigned char* otherCodeBookSeed = (const unsigned char*)"PaladinDu1601022142";
	pCodeBook3->InitSeed(otherCodeBookSeed, 19,key, &keyLen);
	//case "aaaaaaaaaaaaaaaaaaaaaaa" encryptionData "~-a>G!/_]WTw74^.hvisz_1"
	const char* caseTestData = "aaaaaaaaaaaaaaaaaaaaaaa";
	const char* caseEncrptionData = "~-a>G!/_]WTw74^.hvisz_1";
	int caseLen = 23;
	for (int i = 0; i < caseLen; ++i) {
		testData[i] = caseEncrptionData[i];
	}
	testData[caseLen] = '\0';
	pCodeBook3->Decryption(testData, caseLen, key, keyLen);
	bool finishTestOtherCodeBook = true;
	for (int i = 0; i < caseLen; ++i) {
		if (testData[i] != caseTestData[i]) {
			printf("error:%s,%s,%s\n",caseTestData, caseEncrptionData, testData);
			finishTestOtherCodeBook = false;
			break;
		}
	}
	if (finishTestOtherCodeBook) {
		printf("finish test other codebook\n");
	}
	delete pCodeBook;
	delete pCodeBook2;
	delete pCodeBook3;
}