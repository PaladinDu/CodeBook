/*
*@Auth PaladinDu
*@email wsdsc@qq.com
*@note Encrypts str in the specified character set
*/

#pragma once
/**
*@note class not free any param;
*@note class not check any param;
*@note function ret if not null,user need delete it;
*/
class CodeBook {
public :
	CodeBook();

	static CodeBook* InitFromMetaData(const char* metaData,int len);
	/**
	*@note codebook random a map;get same codebook by GetMateData and InitFromMetaData;
	*/
	static CodeBook* RandomInitByValidChars(const unsigned char* validChars, int len);
	/**
	*@note outMetaData must not null and size >=256*4,outValidCharSize ret used len;
	*/
	void GetMateData(char* outMetaData, int* outDataLen);
	/**
	*@note outValidCharsBuffSize256 must not null and size >=256,outValidCharSize ret used len;
	*/
	void GetValidChars(unsigned char* outValidChars, int* outValidCharSize);
	/**
	*@note outKeyData must not null and size >=512 && size >= seed,outKeyLen ret used len;
	*/
	void InitSeed(const unsigned char* seed ,int seedLen,unsigned char* outKeyData,int* outKeyLen);
	/*
	*@note encryption in data self;
	*/
	void Encryption(unsigned char* inAndOutData, int dataLen, unsigned char* key, int keyLen);
	/*
	*@note Decryption in data self;
	*/
	void Decryption(unsigned char* inAndOutData, int dataLen, unsigned char* key, int keyLen);

private:
	unsigned char dataBuff[1024];
	unsigned char* charToIndexMap;
	unsigned char* indexToCharMap;
	unsigned char* encryptionMap; 
	unsigned char* decryptionMap;
	int charsCount;

	void dataToIndex(unsigned char* inAndOutData, int dataLen);
	void indexToData(unsigned char* inAndOutData, int dataLen);
	unsigned char enchange(unsigned char data, int byteKey);
	unsigned char dechange(unsigned char data, int byteKey);
	void encryption(unsigned char* inAndOutData, int dataLen, unsigned char* key, int keyLen);
	void decryption(unsigned char* inAndOutData, int dataLen, unsigned char* key, int keyLen);

};
