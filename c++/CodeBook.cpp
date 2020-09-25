/*
*@Auth PaladinDu
*@email wsdsc@qq.com
*@note Encrypts str in the specified character set
*/

#include "CodeBook.h"
#include "stdlib.h"
#include "time.h"
#define MIN_KEY_LEN 512

const char HexToNumMap[256] = {0, 0, 0, 0, 0, 0, 0, 0,0, 0, 0, 0, 0, 0, 0, 0,
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
const char NumToHexMap[16] = {'0','1','2','3','4','5','6','7','8','9','A','B','C','D','E','F'};


CodeBook::CodeBook() {
	this->charToIndexMap = this->dataBuff;
	this->indexToCharMap = this->charToIndexMap + 256;
	this->encryptionMap = this->indexToCharMap + 256;
	this->decryptionMap = this->encryptionMap + 256;
	this->charsCount = 0;//invalid
}

CodeBook* CodeBook::RandomInitByValidChars(const unsigned char* validChars, int len) {
	CodeBook* ret = new CodeBook();
	bool charUsed[256] = { false };
	for (int i = 0; i < len; ++i) {
		charUsed[validChars[i]] = true;
	}
	for (int i = 0; i < 256; ++i) {
		if (charUsed[i]) {
			ret->charToIndexMap[i] = ret->charsCount;
			ret->indexToCharMap[ret->charsCount] = i;
			ret->encryptionMap[ret->charsCount] = ret->charsCount;
			ret->charsCount += 1;
		}
	}
	//random encryptionMap
	srand(time(NULL));
	for (int i = 0; i < ret->charsCount; ++i) {
		unsigned char randNum = rand() % (ret->charsCount - i);
		unsigned char tmp = ret->encryptionMap[i];
		ret->encryptionMap[i] = ret->encryptionMap[randNum + i];
		ret->decryptionMap[ret->encryptionMap[i]] = i;
		ret->encryptionMap[randNum + i] = tmp;
		
	}
	return ret;
}

CodeBook* CodeBook::InitFromMetaData(const char* metaData, int len) {
	CodeBook* ret = new CodeBook();
	ret->charsCount = (len >> 2);
	const char* validCharsMeta = metaData;
	const char* charChangeMeta = metaData + ret->charsCount * 2;
	for (int i = 0; i < ret->charsCount; ++i) {
		unsigned char tmpChar = ((HexToNumMap[validCharsMeta[i * 2]] << 4) | HexToNumMap[validCharsMeta[i * 2 + 1]]);
		ret->charToIndexMap[tmpChar] = i;
		ret->indexToCharMap[i] = tmpChar;
		tmpChar = ((HexToNumMap[charChangeMeta[i * 2]] << 4) | HexToNumMap[charChangeMeta[i * 2 + 1]]);
		ret->encryptionMap[i] = tmpChar;
		ret->decryptionMap[tmpChar] = i;
	}
	return ret;
}

void CodeBook::GetValidChars(unsigned char* outValidChars, int* outValidCharSize) {
	*outValidCharSize = this->charsCount;
	for (int i = 0; i < this->charsCount; ++i) {
		outValidCharSize[i] = this->indexToCharMap[i];
	}
}
void CodeBook::GetMateData(char* outMetaData, int* outDataLen) {
	int metaDataLen = this->charsCount * 4;
	*outDataLen = metaDataLen;
	char* validCharsMeta = outMetaData;
	char* charChangeMeta = validCharsMeta + this->charsCount * 2;
	for (int i = 0; i < this->charsCount; ++i) {
		validCharsMeta[i * 2] = NumToHexMap[this->indexToCharMap[i] >> 4];
		validCharsMeta[i * 2+1] = NumToHexMap[this->indexToCharMap[i] & 0x0f];
		charChangeMeta[i * 2] = NumToHexMap[this->encryptionMap[i] >> 4];
		charChangeMeta[i * 2 + 1] = NumToHexMap[this->encryptionMap[i] & 0x0f];
	}
}

void CodeBook::InitSeed(const unsigned char* seed, int seedLen, unsigned char* outKeyData, int* outKeyLen) {
	for (int i = 0; i < seedLen; ++i) {
		outKeyData[i] = seed[i];
	}
	if (seedLen < MIN_KEY_LEN) {
		for (int i = seedLen; i < MIN_KEY_LEN; ++i) {
			outKeyData[i] = 0;
		}
		*outKeyLen = MIN_KEY_LEN;
		
	}else {
		*outKeyLen = seedLen;
	}
	int keyLen = *outKeyLen;
	unsigned char tmpCharKey = 0;
	for (int i = 0; i < keyLen; ++i) {
		tmpCharKey = (tmpCharKey + outKeyData[i] + i) % this->charsCount;
		outKeyData[i] = this->enchange(outKeyData[i], tmpCharKey);
	}
	for (int i = 0; i < keyLen; ++i) {
		outKeyData[i] = this->enchange(outKeyData[i], tmpCharKey);
		tmpCharKey = (tmpCharKey + outKeyData[i] + i) % this->charsCount;
	}
}
void CodeBook::Encryption(unsigned char* inAndOutData, int dataLen, unsigned char* key, int keyLen) {
	this->dataToIndex(inAndOutData, dataLen);
	this->encryption(inAndOutData, dataLen, key, keyLen);
	this->indexToData(inAndOutData, dataLen);
}
void CodeBook::Decryption(unsigned char* inAndOutData, int dataLen, unsigned char* key, int keyLen) {
	this->dataToIndex(inAndOutData, dataLen);
	this->decryption(inAndOutData, dataLen, key, keyLen);
	this->indexToData(inAndOutData, dataLen);
}

void CodeBook::dataToIndex(unsigned char* inAndOutData, int dataLen) {
	for (int i = 0; i < dataLen; ++i) {
		inAndOutData[i] = this->charToIndexMap[inAndOutData[i]];
	}
}
void CodeBook::indexToData(unsigned char* inAndOutData, int dataLen) {
	for (int i = 0; i < dataLen; ++i) {
		inAndOutData[i] = this->indexToCharMap[inAndOutData[i]];
	}
}
unsigned char CodeBook::enchange(unsigned char data, int byteKey) {
	return this->encryptionMap[(data+byteKey)%this->charsCount];
}

unsigned char CodeBook::dechange(unsigned char data, int byteKey) {
	return (this->decryptionMap[data]+this->charsCount - byteKey%this->charsCount) % this->charsCount;
}
void CodeBook::encryption(unsigned char* inAndOutData, int dataLen, unsigned char* key, int keyLen) {
	for (int i = 0; i < keyLen; ++i) {
		int dataIndex = i % dataLen;
		inAndOutData[dataIndex] = this->enchange(inAndOutData[dataIndex], key[i]);
	}
	int keyIndex = 0;
	unsigned char tmpCharKey = key[keyIndex];
	for (int i = 0; i < dataLen; ++i) {
		inAndOutData[i] = this->enchange(inAndOutData[i], tmpCharKey);
		keyIndex = keyIndex >= keyLen - 1 ? 0 : keyIndex + 1;
		tmpCharKey = (key[keyIndex] + inAndOutData[i]) % this->charsCount;
	}
	tmpCharKey = key[keyIndex];
	for (int i = dataLen - 1; i >= 0; --i) {
		inAndOutData[i] = this->enchange(inAndOutData[i], tmpCharKey);
		keyIndex = keyIndex >= keyLen - 1 ? 0 : keyIndex + 1;
		tmpCharKey = (key[keyIndex] + inAndOutData[i]) % this->charsCount;
	}
}
void CodeBook::decryption(unsigned char* inAndOutData, int dataLen, unsigned char* key, int keyLen) {
	int keyIndex = (dataLen * 2 - 1) % keyLen;
	for (int i = 0; i < dataLen; ++i) {
		inAndOutData[i] = this->dechange(inAndOutData[i], (key[keyIndex] + (i < dataLen - 1 ? inAndOutData[i + 1] : 0)) % this->charsCount);
		keyIndex = keyIndex == 0 ? keyLen - 1 : keyIndex - 1;
	}
	for (int i = dataLen - 1; i >= 0; --i) {
		inAndOutData[i] = this->dechange(inAndOutData[i],(key[keyIndex]+(i > 0? inAndOutData[i-1] : 0)) % this->charsCount);
		keyIndex = keyIndex == 0 ? keyLen - 1 : keyIndex - 1;
	}
	for (int i = keyLen - 1; i >= 0;--i) {
		int dataIndex = i % dataLen;
		inAndOutData[dataIndex] = this->dechange(inAndOutData[dataIndex], key[i]);
	}
}