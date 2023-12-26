from ArithmeticAlgorithms import Mod_Rq, Mod_S3

n = 701
q = 8192
logq = 13

def Rq_to_bits(a):
  global n, q, logq
  v = Mod_Rq(a)
  b = ''
  i = 0
  while i <= n - 2:
    b += bin(v[i])[2:].zfill(logq)
    i += 1
  return b

def Rq_from_bits(b):
  global n, logq
  b = [0] + b
  v = [0] * n
  i = 0
  while i <= n - 2:
    c = int(b[(i * logq + 1):(i * logq + 14)], 2)
    v[i] = c
    v[-1] -= c
    i += 1
  return Mod_Rq(v)

def S3_to_bits(a):
  v = Mod_S3(a)
  b = ''
  i = 0
  while i < (n - 1) / 5:
    c = 0
    for j in range(1, 6):
      c = (v[5 * i + j] % 3) * 3 ** (5 - j)
    b += bin(c)[2:].zfill(8)
    i += 1
  return b

def S3_from_bits(a):
  b = [0]
  i = 0
  while i < (n - 1) / 5:
    c = int(b[(5 * i + 1):(5 * i + 5)], 2)
    for j in range(5, 0, -1):
      b[5 * i + j] = c % 3
      c //= 3
    i += 1
  return Mod_S3(b)
