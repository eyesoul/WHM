#include "aes128.h"

#include<iostream>
#include<iomanip>
#include<string>

using namespace std;

int main(){
	char key[] = "\x17\x06\x00\x74\x17\x06\x00\x74\x17\x06\x00\x74\x17\x06\x00\x74";
	char plaintext[] = "\xA0\x01\xA0\x01\xA0\x01\xA0\x01\xA0\x01\xA0\x01\xA0\x01\xA0\x01";
	int plen = strlen(plaintext);
	AES128 aes128Cipher(key);
	byte pBlock[16], cBlock[16];
	for(int block=0; ; block++){
		if((block+1)*16>plen)
			break;
		cout<<"Block number: "<<block<<endl;
		cout<<"Input: ";
		for(int i=0; i<16; i++){
			pBlock[i]=(byte)plaintext[block+i];
			cout<<setfill('0')<<setw(2)<<hex<<(unsigned int)pBlock[i]<<" ";
		}
		cout<<endl;
		aes128Cipher.encrypt(pBlock, cBlock);
		cout<<"Output: ";
		for(int i=0; i<16; i++){
			cout<<setfill('0')<<setw(2)<<hex<<(unsigned int)cBlock[i]<<" ";
		}
		cout<<endl;
	}
	return 0;
}