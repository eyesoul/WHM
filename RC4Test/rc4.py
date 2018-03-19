import sys
import base64


def showBytesInHex(bytesStr):
    print("b'%s'" % ''.join('\\x%.2x' % x for x in bytesStr))


class Rc4Cipher:
    def __init__(self, key):
        self.key256 = bytearray(256)
        self.state256 = bytearray(256)
        self.i = 0
        self.j = 0
        for i in range(256):
            self.state256[i] = i
            self.key256[i] = key[i % len(key)]

        j = 0
        for i in range(256):
            j = (j+self.state256[i]+self.key256[i]) % 256
            tmp = self.state256[i]
            self.state256[i] = self.state256[j]
            self.state256[j] = tmp

        self.state256Save = bytearray(256)
        for i in range(256):
            self.state256Save[i] = self.state256[i]   # 保存状态，留待解码
        print("Initiate successfully")
#        print(self.state256[7], self.state256[199])
#        print(self.state256)

    def streamByteGen(self):
        self.i = (self.i+1) % 256
        self.j = (self.j+self.state256[self.i]) % 256
        tmp = self.state256[self.i]
        self.state256[self.i] = self.state256[self.j]
        self.state256[self.j] = tmp
        t = (self.state256[self.i] + self.state256[self.j]) % 256
        return self.state256[t]

    def encrypt(self, plaintext):
        self.i = 0
        self.j = 0
        for i in range(256):
            self.state256[i] = self.state256Save[i]   # 保存状态，留待解码
        ciphertext = bytearray(len(plaintext))
        for i in range(len(plaintext)):
            ciphertext[i] = plaintext[i] ^ self.streamByteGen()
        return ciphertext

    def decrypt(self, ciphertext):
        self.i = 0
        self.j = 0
        for i in range(256):
            self.state256[i] = self.state256Save[i]   # 保存状态，留待解码
        plaintext = bytearray(len(ciphertext))
        for i in range(len(ciphertext)):
            plaintext[i] = ciphertext[i] ^ self.streamByteGen()
        return plaintext


if __name__ == '__main__':
    if len(sys.argv) < 3:
        sys.exit("Parameter error! Goodbye!")
    waitingEncryptFileName = sys.argv[1]
    key = str.encode(sys.argv[2])

    try:
        waitingEncryptFile = open(waitingEncryptFileName, 'rb')
    except IOError:
        sys.exit("Error occurred. Can't open file %s" % waitingEncryptFileName)

    ciphertext = b''
    plaintext = waitingEncryptFile.read()
    print("The plaintext is: %s" % plaintext)
    rc4 = Rc4Cipher(key)
    ciphertext = rc4.encrypt(plaintext)
    print("The ciphertext is: ")
    print(base64.b64encode(ciphertext))
    showBytesInHex(ciphertext)
    print(rc4.decrypt(ciphertext))
    waitingEncryptFile.close()
