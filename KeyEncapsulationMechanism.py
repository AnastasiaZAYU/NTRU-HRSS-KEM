from SamplingAlgorithms import Sample_Tplus, Sample_T
from ArithmeticAlgorithms import *
from EncodingAlgorithms import *
from ExternallyAlgorithms import SHAKE128
import random

n = 701
seed_bits = 256
coin_bits = 256
shared_key_bits = 256
q = 8192
s3_packed_bits = 1120
owcpa_public_key_bits = 9100
owcpa_private_key_bits = 2240
owcpa_ciphertext_bits = 9100
cca_public_key_bits = 9100
cca_private_key_bits = 10220
cca_ciphertext_bits = 10220

def Generate_Key():
  global seed_bits
  seed = ''.join(random.choice('01') for _ in range(seed_bits))
  f, fp = Generate_Private_Key(seed)
  h = Generate_Public_Key(seed, f)
  packed_public_key = Rq_to_bits(h)
  packed_private_key = S3_to_bits(f) + S3_to_bits(fp)
  return packed_public_key, packed_private_key

def Generate_Private_Key(seed):
  domf = '0100000000000000'
  f = Sample_Tplus(seed, domf)
  fp = S3_inverse(f)
  return f, fp

def Generate_Public_Key(seed, f):
  global q
  domg = '0200000000000000'
  v0 = Sample_Tplus(seed, domg)
  g = S3_to_Zx(v0)
  v1 = Sq_inverse(f)
  fq = Sq_to_Zx(v1)
  v2 = Multiply(g, fq, q)
  v2 = Multiply([-3, 3], v2, q)
  h = Mod_Rq(v2)
  return h

def Encapsulate(packed_public_key):
  global seed_bits, coin_bits, shared_key_bits, s3_packed_bits
  seed = ''.join(random.choice('01') for _ in range(seed_bits))
  domm ='0000000000000000'
  m = Sample_T(seed, domm)
  packed_m = S3_to_bits(m)
  hashes = SHAKE128(packed_m, coin_bits + shared_key_bits + s3_packed_bits)
  coins = hashes[:coin_bits]
  shared_key = hashes[coin_bits:coin_bits + shared_key_bits]
  qrom_hash = hashes[coin_bits + shared_key_bits:]
  packed_owcpa_ct = NTRU_OWF_Public(packed_m, packed_public_key, coins)
  packed_cca_ct = packed_owcpa_ct + qrom_hash
  return shared_key, packed_cca_ct

def Decapsulate(packed_key_pair, packed_cca_ct):
  global owcpa_private_key_bits, owcpa_public_key_bits, owcpa_ciphertext_bits, s3_packed_bits, coin_bits, shared_key_bits, s3_packed_bits, n
  packed_private_key = packed_key_pair[:owcpa_private_key_bits]
  packed_public_key = packed_key_pair[owcpa_private_key_bits:]
  packed_owcpa_ct = packed_cca_ct[:owcpa_ciphertext_bits]
  qrom_hash = packed_cca_ct[owcpa_ciphertext_bits:]
  packed_m = NTRU_OWF_Private(packed_private_key, packed_owcpa_ct)
  hashes = SHAKE128(packed_m, coin_bits + shared_key_bits + s3_packed_bits)
  coins = hashes[:coin_bits]
  shared_key = hashes[coin_bits:coin_bits + shared_key_bits]
  re_qrom_hash = hashes[coin_bits + shared_key_bits:]
  re_packed_owcpa_ct = NTRU_OWF_Public(n, packed_m, packed_public_key, coins)
  if re_packed_owcpa_ct + re_qrom_hash == packed_owcpa_ct + qrom_hash:
    return shared_key
  else:
    return [0] * len(shared_key_bits)

def NTRU_OWF_Public(packed_m, packed_public_key, coins):
  h = Rq_from_bits(packed_public_key)
  domr = '0000000000000000'
  v0 = Sample_T(coins, domr)
  r = S3_to_Zx(v0)
  v1 = S3_from_bits(packed_m)
  m = S3_to_R(v1)
  e = Multiply(r, h, q)
  e = Addition(e, m, q)
  e = Mod_Rq(e)
  packed_owcpa_ct = Rq_to_bits(e)
  return packed_owcpa_ct

def NTRU_OWF_Private(packed_private_key, packed_owcpa_ct):
  global s3_packed_bits, owcpa_ciphertext_bits
  packed_f = packed_private_key[:s3_packed_bits]
  packed_fp = packed_private_key[s3_packed_bits:]
  qrom_hash = packed_owcpa_ct[owcpa_ciphertext_bits:]
  packed_owcpa_ct = packed_owcpa_ct[:owcpa_ciphertext_bits]
  e = Rq_from_bits(packed_owcpa_ct)
  v0 = S3_from_bits(packed_f)
  f = S3_to_Zx(v0)
  fp = S3_from_bits(packed_fp)
  v1 = Multiply(e, f, q)
  v1 = Mod_Rq(v1)
  v2 = Multiply(v1, fp)
  v2 = Mod_S3(v1)
  packed_m = S3_to_bits(v2)
  return packed_m
