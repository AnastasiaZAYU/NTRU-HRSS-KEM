import math
import binascii
import sys
sys.set_int_max_str_digits(0)

def SHAKE128(M, d):
  M = M + '1111'
  b = GetHash(M, 1088, 512, d // 12)
  b = toBinary(b)
  b = '0' * (d - len(b)) + b
  return b

RC =[0x0000000000000001,
        0x0000000000008082,
        0x800000000000808A,
        0x8000000080008000,
        0x000000000000808B,
        0x0000000080000001,
        0x8000000080008081,
        0x8000000000008009,
        0x000000000000008A,
        0x0000000000000088,
        0x0000000080008009,
        0x000000008000000A,
        0x000000008000808B,
        0x800000000000008B,
        0x8000000000008089,
        0x8000000000008003,
        0x8000000000008002,
        0x8000000000000080,
        0x000000000000800A,
        0x800000008000000A,
        0x8000000080008081,
        0x8000000000008080,
        0x0000000080000001,
        0x8000000080008008]
r = [[0,    36,     3,    41,    18]     ,
                          [1,    44,    10,    45,     2]    ,
                          [62,    6,    43,    15,    61]    ,
                          [28,   55,    25,    21,    56]    ,
                          [27,   20,    39,     8,    14]    ]
b = 1600
w = b / 25
l = math.log(w, 2)
n = 12 + 2 * l

def rot(x, n):
    n = n % w
    return (((int(x) << int(n)) | (int(x) >> int((w - n)))))

def roundB(A, RC):
    C = []
    D = []
    B = [[0] * 5 for _ in range(5)]
    for i in range (0, 5):
        C.append(A[i][0] ^ A[i][1] ^ A[i][2] ^ A[i][3] ^ A[i][4])
    for i in range (0, 5):
        D.append(C[(i + 4) % 5] ^ rot(C[(i + 1) % 5], 1))
    for i in range (0, 5):
        for j in range (0, 5):
            A[i][j] = A[i][j] ^ D[i]
    for i in range (0, 5):
        for j in range (0, 5):
            B[j].insert((2 * i + 3 * j) % 5, rot(A[i][j], r[i][j]))
    for i in range (0, 5):
        for j in range (0, 5):
            A[i][j] = B[i][j] ^ ((~B[((i + 1) % 5)][j]) & B[int((i + 2) % 5)][j])
    A[0][0] = A[0][0] ^ RC;
    return A

def Keccackf(A):
    for i in range (0, 5):
        A = roundB(A, RC[i]);
    return A

def padding(M, r):
    size = 0;
    M = M + "01"
    while (((len(M) / 2) * 8 % r) != ((r - 8))):
        M = M + "00"
    M = M + "80"
    size = (((len(M) / 2) * 8) / r);
    arrayM = [[]]
    temp = ""
    count = 0;
    j = 0;
    i = 0;
    for ch in M:
        if (j > (r / w - 1)):
            j = 0
            i += 1
        count += 1
        if (int(count * 4 % w) == 0):
            start_index = int((count - w / 4))
            end_index = start_index + int(w / 4)
            arrayM[i].append(int(M[start_index:end_index], 16))
            temp = ToReverseHexString(arrayM[i][j])
            arrayM[i][j] = int(temp)
            j += 1
    return arrayM

def ToReverseHexString(S):
    temp = binascii.hexlify(int.to_bytes(int(str(S), 16), length=(len(str(S)) + 1) // 2, byteorder='big')).decode('utf-8')
    return temp

def ToHexString(S):
    temp = binascii.hexlify(bytearray(S, 'utf-8')[::-1]).decode()
    return temp

def GetHash(M, r, c, d):
    S = []
    for i in range(5):
        row = []
        for j in range(5):
            row.append(0)
        S.append(row)
    P = padding(M, r)
    for Pi in P:
        for i in range (0, 5):
            for j in range (0, 5):
                if ((i + j * 5) < (r / w)):
                    S[i][j] = S[i][j] ^ Pi[i + j * 5]
    Z = ""
    while (len(Z) < (d * 2)):
        for i in range (0, 5):
            for j in range (0, 5):
                if ((5 * i + j) < (r / w)):
                    Z = Z + ToReverseHexString(S[j][i])
        Keccackf(S)
    return Z[0:(d * 2)]

def toBinary(a):
  l,m=[],[]
  for i in a:
    l.append(ord(i))
  for i in l:
    m.append(int(bin(i)[2:]))
  mu = [str(i) for i in m]
  delimiter = ''
  mi = delimiter.join(mu)
  return mi
