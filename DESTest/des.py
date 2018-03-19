import sys
import base64

IPTable = [
    58, 50, 42, 34, 26, 18, 10, 2,
    60, 52, 44, 36, 28, 20, 12, 4,
    62, 54, 46, 38, 30, 22, 14, 6,
    64, 56, 48, 40, 32, 24, 16, 8,
    57, 49, 41, 33, 25, 17, 9, 1,
    59, 51, 43, 35, 27, 19, 11, 3,
    61, 53, 45, 37, 29, 21, 13, 5,
    63, 55, 47, 39, 31, 23, 15, 7
]

IP_1Table = [
    40, 8, 48, 16, 56, 24, 64, 32,
    39, 7, 47, 15, 55, 23, 63, 31,
    38, 6, 46, 14, 54, 22, 62, 30,
    37, 5, 45, 13, 53, 21, 61, 29,
    36, 4, 44, 12, 52, 20, 60, 28,
    35, 3, 43, 11, 51, 19, 59, 27,
    34, 2, 42, 10, 50, 18, 58, 26,
    33, 1, 41, 9, 49, 17, 57, 25
]

ExpandTable = [
    32, 1, 2, 3, 4, 5,
    4, 5, 6, 7, 8, 9,
    8, 9, 10, 11, 12, 13,
    12, 13, 14, 15, 16, 17,
    16, 17, 18, 19, 20, 21,
    20, 21, 22, 23, 24, 25,
    24, 25, 26, 27, 28, 29,
    28, 29, 30, 31, 32, 1
]

PSwapTable = [
    16, 7, 20, 21, 29, 12, 28, 17,
    1, 15, 23, 26, 5, 18, 31, 10,
    2, 8, 24, 14, 32, 27, 3, 9,
    19, 13, 30, 6, 22, 11, 4, 25
]
PC1SwapTable = [
    57, 49, 41, 33, 25, 17, 9,
    1, 58, 50, 42, 34, 26, 18,
    10, 2, 59, 51, 43, 35, 27,
    19, 11, 3, 60, 52, 44, 36,
    63, 55, 47, 39, 31, 23, 15,
    7, 62, 54, 46, 38, 30, 22,
    14, 6, 61, 53, 45, 37, 29,
    21, 13, 5, 28, 20, 12, 4
]
PC2SwapTable = [
    14, 17, 11, 24, 1, 5,
    3, 28, 15, 6, 21, 10,
    23, 19, 12, 4, 26, 8,
    16, 7, 27, 20, 13, 2,
    41, 52, 31, 37, 47, 55,
    30, 40, 51, 45, 33, 48,
    44, 49, 39, 56, 34, 53,
    46, 42, 50, 36, 29, 32
]

KeyGenTables = [
    [
        10, 51, 34, 60, 49, 17, 33, 57, 2, 9, 19, 42,
        3, 35, 26, 25, 44, 58, 59, 1, 36, 27, 18, 41,
        22, 28, 39, 54, 37, 4, 47, 30, 5, 53, 23, 29,
        61, 21, 38, 63, 15, 20, 45, 14, 13, 62, 55, 31
    ],     # 1
    [
        2, 43, 26, 52, 41, 9, 25, 49, 59, 1, 11, 34,
        60, 27, 18, 17, 36, 50, 51, 58, 57, 19, 10, 33,
        14, 20, 31, 46, 29, 63, 39, 22, 28, 45, 15, 21,
        53, 13, 30, 55, 7, 12, 37, 6, 5, 54, 47, 23
    ],     # 2
    [
        51, 27, 10, 36, 25, 58, 9, 33, 43, 50, 60, 18,
        44, 11, 2, 1, 49, 34, 35, 42, 41, 3, 59, 17,
        61, 4, 15, 30, 13, 47, 23, 6, 12, 29, 62, 5,
        37, 28, 14, 39, 54, 63, 21, 53, 20, 38, 31, 7
    ],     # 3
    [
        35, 11, 59, 49, 9, 42, 58, 17, 27, 34, 44, 2,
        57, 60, 51, 50, 33, 18, 19, 26, 25, 52, 43, 1,
        45, 55, 62, 14, 28, 31, 7, 53, 63, 13, 46, 20,
        21, 12, 61, 23, 38, 47, 5, 37, 4, 22, 15, 54
    ],     # 4
    [
        19, 60, 43, 33, 58, 26, 42, 1, 11, 18, 57, 51,
        41, 44, 35, 34, 17, 2, 3, 10, 9, 36, 27, 50,
        29, 39, 46, 61, 12, 15, 54, 37, 47, 28, 30, 4,
        5, 63, 45, 7, 22, 31, 20, 21, 55, 6, 62, 38
    ],     # 5
    [
        3, 44, 27, 17, 42, 10, 26, 50, 60, 2, 41, 35,
        25, 57, 19, 18, 1, 51, 52, 59, 58, 49, 11, 34,
        13, 23, 30, 45, 63, 62, 38, 21, 31, 12, 14, 55,
        20, 47, 29, 54, 6, 15, 4, 5, 39, 53, 46, 22
    ],     # 6
    [
        52, 57, 11, 1, 26, 59, 10, 34, 44, 51, 25, 19,
        9, 41, 3, 2, 50, 35, 36, 43, 42, 33, 60, 18,
        28, 7, 14, 29, 47, 46, 22, 5, 15, 63, 61, 39,
        4, 31, 13, 38, 53, 62, 55, 20, 23, 37, 30, 6
    ],     # 7
    [
        36, 41, 60, 50, 10, 43, 59, 18, 57, 35, 9, 3,
        58, 25, 52, 51, 34, 19, 49, 27, 26, 17, 44, 2,
        12, 54, 61, 13, 31, 30, 6, 20, 62, 47, 45, 23,
        55, 15, 28, 22, 37, 46, 39, 4, 7, 21, 14, 53
    ],     # 8
    [
        57, 33, 52, 42, 2, 35, 51, 10, 49, 27, 1, 60,
        50, 17, 44, 43, 26, 11, 41, 19, 18, 9, 36, 59,
        4, 46, 53, 55, 23, 22, 61, 12, 54, 39, 37, 15,
        47, 7, 20, 14, 29, 38, 31, 63, 62, 13, 6, 45
    ],     # 9
    [
        41, 17, 36, 26, 51, 19, 35, 59, 33, 11, 50, 44,
        34, 1, 57, 27, 10, 60, 25, 3, 2, 58, 49, 43,
        55, 30, 37, 20, 7, 6, 45, 63, 38, 23, 21, 62,
        31, 34, 4, 61, 13, 22, 15, 47, 46, 28, 53, 29
    ],     # 10
    [
        25, 1, 49, 10, 35, 3, 19, 43, 17, 60, 34, 57,
        18, 50, 41, 11, 59, 44, 9, 52, 51, 42, 33, 27,
        39, 14, 21, 4, 54, 53, 29, 47, 22, 7, 5, 46,
        15, 38, 55, 45, 28, 6, 62, 31, 30, 12, 37, 13
    ],     # 11
    [
        9, 50, 33, 59, 19, 52, 3, 27, 1, 44, 18, 41,
        2, 34, 25, 60, 43, 57, 58, 36, 35, 26, 17, 11,
        23, 61, 5, 55, 38, 37, 13, 31, 6, 54, 20, 30,
        62, 22, 39, 29, 12, 53, 46, 15, 14, 63, 21, 28
    ],     # 12
    [
        58, 34, 17, 43, 3, 36, 52, 11, 50, 57, 2, 35,
        51, 18, 9, 44, 27, 41, 42, 49, 19, 10, 1, 60,
        7, 45, 20, 39, 22, 21, 28, 15, 53, 38, 4, 14,
        46, 6, 23, 13, 63, 37, 30, 62, 61, 47, 5, 12
    ],     # 13
    [
        42, 18, 1, 27, 52, 49, 36, 60, 34, 41, 51, 9,
        35, 2, 58, 57, 11, 25, 26, 33, 3, 59, 50, 44,
        54, 29, 4, 23, 6, 5, 12, 62, 37, 22, 55, 61,
        30, 53, 7, 28, 47, 21, 14, 46, 45, 31, 20, 63
    ],     # 14
    [
        26, 2, 50, 11, 36, 33, 49, 44, 18, 25, 35, 58,
        19, 51, 42, 41, 60, 9, 10, 17, 52, 43, 34, 57,
        38, 13, 55, 7, 53, 20, 63, 46, 21, 6, 39, 45,
        14, 37, 54, 12, 31, 5, 61, 30, 29, 15, 4, 47
    ],     # 15
    [
        18, 59, 42, 3, 57, 25, 41, 36, 10, 17, 27, 50,
        11, 43, 34, 33, 52, 1, 2, 9, 44, 35, 26, 49,
        30, 5, 47, 62, 45, 12, 55, 38, 13, 61, 31, 37,
        6, 29, 46, 4, 23, 28, 53, 22, 21, 7, 63, 39
    ]     # 16
]

S1 = [
    [14, 4, 13, 1, 2, 15, 11, 8, 3, 10, 6, 12, 5, 9, 0, 7],
    [0, 15, 7, 4, 15, 2, 13, 1, 10, 6, 12, 11, 9, 5, 3, 8],
    [4, 1, 14, 8, 13, 6, 2, 11, 15, 12, 9, 7, 3, 10, 5, 0],
    [15, 12, 8, 2, 4, 9, 1, 7, 5, 11, 3, 14, 10, 0, 6, 13]
]
S2 = [
    [15, 1, 8, 14, 6, 11, 3, 4, 9, 7, 2, 13, 12, 0, 5, 10],
    [3, 13, 4, 7, 15, 2, 8, 14, 12, 0, 1, 10, 6, 9, 11, 5],
    [0, 14, 7, 11, 10, 4, 13, 1, 5, 8, 12, 6, 9, 3, 2, 15],
    [13, 8, 10, 1, 3, 15, 4, 2, 11, 6, 7, 12, 0, 5, 14, 9]
]
S3 = [
    [10, 0, 9, 14, 6, 3, 15, 5, 1, 13, 12, 7, 11, 4, 2, 8],
    [13, 7, 0, 9, 3, 4, 6, 10, 2, 8, 5, 14, 12, 11, 15, 1],
    [13, 6, 4, 9, 8, 15, 3, 0, 11, 1, 2, 12, 5, 10, 14, 7],
    [1, 10, 13, 0, 6, 9, 8, 7, 4, 15, 14, 3, 11, 5, 2, 12]
]
S4 = [
    [7, 13, 14, 3, 0, 6, 9, 10, 1, 2, 8, 5, 11, 12, 4, 15],
    [12, 8, 11, 5, 6, 15, 0, 3, 4, 7, 2, 12, 1, 10, 14, 9],
    [10, 6, 9, 0, 12, 11, 7, 13, 15, 1, 3, 14, 5, 2, 8, 4],
    [3, 15, 0, 6, 10, 1, 13, 8, 9, 4, 5, 11, 12, 7, 2, 14]
]
S5 = [
    [2, 12, 4, 1, 7, 10, 11, 6, 8, 5, 3, 15, 13, 0, 14, 9],
    [14, 11, 2, 12, 4, 7, 13, 1, 5, 0, 15, 10, 3, 9, 8, 6],
    [4, 2, 1, 11, 10, 13, 7, 8, 15, 9, 12, 5, 6, 3, 0, 14],
    [11, 8, 12, 7, 1, 14, 2, 13, 6, 15, 0, 9, 10, 4, 5, 3]
]
S6 = [
    [12, 1, 10, 15, 9, 2, 6, 8, 0, 13, 3, 4, 14, 7, 5, 11],
    [10, 15, 4, 2, 7, 12, 9, 5, 6, 1, 13, 14, 0, 11, 3, 8],
    [9, 14, 15, 5, 2, 8, 12, 3, 7, 0, 4, 10, 1, 13, 11, 6],
    [4, 3, 2, 12, 9, 5, 15, 10, 11, 14, 1, 7, 6, 0, 8, 13]
]
S7 = [
    [4, 11, 2, 14, 15, 0, 8, 13, 3, 12, 9, 7, 5, 10, 6, 1],
    [13, 0, 11, 7, 4, 9, 1, 10, 14, 3, 5, 12, 2, 15, 8, 6],
    [1, 4, 11, 13, 12, 3, 7, 14, 10, 15, 6, 8, 0, 5, 9, 2],
    [6, 11, 13, 8, 1, 4, 10, 7, 9, 5, 0, 15, 14, 2, 3, 12]
]
S8 = [
    [13, 2, 8, 4, 6, 15, 11, 1, 10, 9, 3, 14, 5, 0, 12, 7],
    [1, 15, 13, 8, 10, 3, 7, 4, 12, 5, 6, 11, 0, 14, 9, 2],
    [7, 11, 4, 1, 9, 12, 14, 2, 0, 6, 10, 13, 15, 3, 5, 8],
    [2, 1, 14, 7, 4, 10, 8, 13, 15, 12, 9, 0, 3, 5, 6, 11]
]


class DesCipher:
    def __init__(self, key):
        if len(key) != 8:
            sys.exit("Please give 8 bytes key!")
        self.roundNumber = 16
        self.blockBitSize = 64
        self.blockByteSize = self.blockBitSize//8
        self.keyLen = 48
        self.encryptKeys = \
            [bytearray(self.keyLen//8) for i in range(self.roundNumber)]
        self.decryptKeys = \
            [bytearray(self.keyLen//8) for i in range(self.roundNumber)]
        self.leftBlock = bytearray(self.blockByteSize//2)
        self.rightBlock = bytearray(self.blockByteSize//2)
        # Initiate keys
        for i in range(self.roundNumber):
            key48 = bytearray(self.keyLen//8)
            self.swapFunc(key, key48, KeyGenTables[i])
            for j in range(self.keyLen//8):
                self.encryptKeys[i][j] = key48[j]
                self.decryptKeys[self.roundNumber-i-1][j] = key48[j]
        showBytesInHex(self.encryptKeys[0])

    def encrypt(self, plaintext):
        ciphertext = b''
        plaintextBlock = bytearray(self.blockByteSize)
        blockNumber = len(plaintext)//self.blockByteSize
        pkcs7Stuff = 8 - (len(plaintext) - blockNumber*self.blockByteSize)
        if pkcs7Stuff > 0:
            blockNumber += 1
        for b in range(blockNumber):
            if b == (blockNumber-1):    # 字符填充
                for i in range(self.blockByteSize-pkcs7Stuff):
                    plaintextBlock[i] = \
                        plaintext[b*self.blockByteSize+i]
                for i in range(
                    self.blockByteSize-pkcs7Stuff,
                    self.blockByteSize
                ):
                    plaintextBlock[i] = pkcs7Stuff
            else:
                for i in range(self.blockByteSize):
                    plaintextBlock[i] = \
                        plaintext[b*self.blockByteSize+i]
            self.swapFunc(plaintextBlock, plaintextBlock, IPTable)
            ciphertextBlock = self.getFeistelOutput(    # 加密明文块
                plaintextBlock, self.encryptKeys)
            self.swapFunc(ciphertextBlock, ciphertextBlock, IP_1Table)
            ciphertext += ciphertextBlock
        return ciphertext

    def decrypt(self, ciphertext):
        plaintext = b''
        ciphertextBlock = bytearray(self.blockByteSize)
        blockNumber = len(ciphertext)//self.blockByteSize
        if (len(ciphertext) % self.blockByteSize) > 0:
            sys.exit("The ciphertext is incorrect")
        for b in range(blockNumber):
            for i in range(self.blockByteSize):
                ciphertextBlock[i] = ciphertext[b*self.blockByteSize+i]
            self.swapFunc(ciphertextBlock, ciphertextBlock, IPTable)
            plaintextBlock = self.getFeistelOutput(    # 加密明文块
                ciphertextBlock, self.decryptKeys)
            self.swapFunc(plaintextBlock, plaintextBlock, IP_1Table)
            plaintext += plaintextBlock
        return plaintext

    def getFeistelOutput(self, inputBlock, keys):
        tmpBlock = bytearray(self.blockByteSize//2)
        for i in range(self.blockByteSize//2):   # 分左右两块
            self.leftBlock[i] = inputBlock[i]
            self.rightBlock[i] = inputBlock[self.blockByteSize//2 + i]

        # 开始进入Feistel结构
        for r in range(self.roundNumber):   # 进入16轮加密运算
            for i in range(self.blockByteSize//2):   # 暂存右块
                tmpBlock[i] = self.rightBlock[i]
            # 轮函数运算
            expandBlock = bytearray(self.keyLen//8)
            for i in range(self.keyLen):    # E扩展
                ej = i // 8
                ek = i % 8
                rj = (ExpandTable[i] - 1) // 8
                rk = (ExpandTable[i] - 1) % 8
                expandBlock[ej] |= (((self.rightBlock[rj] >> rk) & 1) << ek)
            # 与密钥异或
            for i in range(self.keyLen//8):
                expandBlock[i] ^= keys[r][i]
            # 取出8个S盒输入
            sIn = []
            sIn.append(expandBlock[0] & 63)
            sIn.append((expandBlock[0] >> 6) | (expandBlock[1] & 15))
            sIn.append((expandBlock[1] >> 4) | (expandBlock[2] & 3))
            sIn.append(expandBlock[2] >> 2)
            sIn.append(expandBlock[3] & 63)
            sIn.append((expandBlock[3] >> 6) | (expandBlock[4] & 15))
            sIn.append((expandBlock[4] >> 4) | (expandBlock[5] & 3))
            sIn.append(expandBlock[5] >> 2)
            # 计算S盒输出
            self.rightBlock[0] = S1[self.getRow(sIn[0])][self.getColum(sIn[0])]
            self.rightBlock[0] |= S2[self.getRow(sIn[1])][
                self.getColum(sIn[1])] << 4
            self.rightBlock[1] = S1[self.getRow(sIn[2])][self.getColum(sIn[2])]
            self.rightBlock[1] |= S2[self.getRow(sIn[3])][
                self.getColum(sIn[3])] << 4
            self.rightBlock[2] = S1[self.getRow(sIn[4])][self.getColum(sIn[4])]
            self.rightBlock[2] |= S2[self.getRow(sIn[5])][
                self.getColum(sIn[5])] << 4
            self.rightBlock[3] = S1[self.getRow(sIn[6])][self.getColum(sIn[6])]
            self.rightBlock[3] |= S2[self.getRow(sIn[7])][
                self.getColum(sIn[7])] << 4
            # P置换
            self.swapFunc(self.rightBlock, self.rightBlock, PSwapTable)
            # 轮函数运算结束
            for i in range(self.blockByteSize//2):   # 异或输出新的左右块
                self.rightBlock[i] ^= self.leftBlock[i]
                self.leftBlock[i] = tmpBlock[i]
        # Feistel结构运算结束

        for i in range(self.blockByteSize//2):   # 最后进行左右块互换
            tmpBlock[i] = self.rightBlock[i]
            self.rightBlock[i] = self.leftBlock[i]
            self.leftBlock[i] = tmpBlock[i]

        return self.leftBlock + self.rightBlock

    def swapFunc(self, sBlock, dBlock, swapTable):
        tmp = bytearray(len(dBlock))
        for i in range(len(swapTable)):
            tj = i // 8
            tk = i % 8
            sj = (swapTable[i] - 1) // 8
            sk = (swapTable[i] - 1) % 8
            tmp[tj] |= ((sBlock[sj] >> sk) & 1) << tk
        for i in range(len(dBlock)):
            dBlock[i] = tmp[i]

    def getRow(self, ss):     # 取出6比特S盒输入中首尾比特组成行序号
        return (ss & 1) | ((ss >> 4) & 2)

    def getColum(self, ss):   # 取出中间4比特组成列序号
        return (ss >> 1) & 15
# DesCipher Over


def showBytesInHex(bytesStr):
    print("b'%s'" % ''.join('\\x%.2x' % x for x in bytesStr))


if __name__ == '__main__':
    des = DesCipher(b'17060074')
    plaintext = "I'm Wu Haomin"
    ciphertext = des.encrypt(str.encode(plaintext, encoding='utf_8'))
    showBytesInHex(ciphertext)
    print(base64.b64encode(ciphertext))
    print(des.decrypt(ciphertext))
