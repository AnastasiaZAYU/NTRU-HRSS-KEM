from ExternallyAlgorithms import SHAKE128
from ArithmeticAlgorithms import Mod_S3

n = 701
k = 2

def Sample_T(seed, domain):
  global n, k
  v = [0] * (n - 1)
  i = 0
  l = 2 * k * (n - 1)
  b = '0' + SHAKE128(domain + seed, l)
  while i < n - 1:
    for j in range(1, k + 1):
      v[i] += int(b[2 * k * i + j]) - int(b[2 * k * i + k + j])
      i += 1
  return Mod_S3(v)

def Sample_Tplus(seed, domain):
  global n
  v = Sample_T(seed, domain)
  t = 0
  for i in range(1, n-1):
    t += v[i] * v[i - 1]
  s = 1
  if t < 0:
    s = -1
  i = 0
  while i < n - 2:
    v[i] *= s
    i += 2
  return Mod_S3(v)
