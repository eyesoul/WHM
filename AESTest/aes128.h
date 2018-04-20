#ifndef AES128_H
#define AES128_H

#define ROUND 11
typedef unsigned char byte;


class AES128{
private:
	byte state[16];
	byte tmpstate[16];
	byte key[16];
	byte subKeys[ROUND][16];


	static const unsigned int Rcon[10];

	static const byte S_box[256];
	static const byte InvS_box[256];

    static const byte GFMatrix[4][4];
    static const byte InvGFMatrix[4][4];

	void keyExpansions();
	byte GFMultiply2(byte b);
	byte GFMultiply(byte a, byte b);

	void addRoundKey(int r);
	void subBytes();
	void invSubBytes();
	void shiftRows();
	void invShiftRows();
	void mixColumns();
	void invMixColumns();

public:
	AES128(const char* k);
	~AES128();
	void encrypt(const byte* p, byte* c);
	void decrypt(const byte* c, byte* p);
};

#endif