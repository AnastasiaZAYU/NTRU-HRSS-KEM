n = 701
q = 8192

def S3_to_R(a):
  global n
  v0 = S3_inverse([-1, 1])
  v1 = Multiply(v0, a, 3)
  v2 = S3_to_Zx(v1)
  b = Multiply([-1, 1], v2, 3)
  b = [-1 if x == 2 else x for x in b]
  return b

def S3_to_Zx(a):
  return Mod_S3(a)

def Sq_to_Zx(a):
  return Mod_Sq(a)

def Rq_to_Zx(a):
  return Mod_Rq(a)

def S2_inverse(a):
  global n
  k = 1
  b = [1]
  c = [0]
  f = a
  g = [-1] + [0] * (n - 1) + [1]
  while f[0] == 0:
    f = f[1:]
    c = [0] + c
    k += 1
  if len(f) < len(g):
    f, g = g, f
    b, c = c, b
  if len(f) == 1 and abs(f[0]) == 1:
    b = [0] * (n - k) + b
    if f[0] == -1:
      b = [-x for x in b]
    b = RemainderDivision(b, [-1] + [0] * (n - 1) + [1], 2)
    return b
  if f[0] == g[0]:
    f = Subtract(f, g, 2)
    b = Subtract(b, c, 2)
  else:
    f = Addition(f, g, 2)
    b = Addition(b, c, 2)
  return b

def S3_inverse(a):
  global n
  k = 1
  b = [1]
  c = [0]
  f = a
  g = [-1] + [0] * (n - 1) + [1]
  while f[0] == 0:
    f = f[1:]
    c = [0] + c
    k += 1
  if len(f) < len(g):
    f, g = g, f
    b, c = c, b
  if len(f) == 1 and abs(f[0]) == 1:
    b = [0] * (n - k) + b
    if f[0] == -1:
      b = [-x for x in b]
    b = RemainderDivision(b, [-1] + [0] * (n - 1) + [1], 3)
    b = [-1 if x == 2 else x for x in b]
    return b
  if f[0] == g[0]:
    f = Subtract(f, g, 3)
    b = Subtract(b, c, 3)
  else:
    f = Addition(f, g, 3)
    b = Addition(b, c, 3)
  b = [-1 if x == 2 else x for x in b]
  return b

def Sq_inverse(a):
  global q
  v0 = S2_inverse(a)
  t = 2
  while t < q:
    c = Multiply(a, v0)
    c = [q - x for x in c]
    c[0] = (c[0] + 2) % q
    c = Multiply(v0, c, q)
    v0 = Mod_Sq(c)
    t *= t
  return v0

def Mod_Sq(a):
  global n
  S = [1] * n
  a = RemainderDivision(a, S, q)
  a = [x % q for x in a]
  a = [x - q if x > q / 2 - 1 else x for x in a]
  return a

def RemainderDivision(a, b, mod):
  while len(a) >= len(b):
    c = [0] * (len(a) - len(b)) + b
    coef = a[-1]
    result = [(x - coef * y) % mod for x, y in zip(a, c)]
    while a and a[-1] == 0:
      a.pop()
  return a

def Multiply(a, b, mod):
  size = len(a) + len(b) - 1
  c = [0] * size
  for i in range(0, len(a)):
    for j in range(0, len(b)):
      c[i + j] += a[i] * b[j];
      c[i + j] %= mod;
  while c and c[-1] == 0:
    c.pop()
  return c

def Subtract(a, b, mod):
  if len(a) < len(b):
    a.extend([0] * (len(b) - len(a)))
  if len(b) < len(a):
    b.extend([0] * (len(a) - len(b)))
  c = [(x - y) % mod for x, y in zip(a, b)]
  while c and c[-1] == 0:
    c.pop()
  return c

def Addition(a, b, mod):
  if len(a) < len(b):
    a.extend([0] * (len(b) - len(a)))
  if len(b) < len(a):
    b.extend([0] * (len(a) - len(b)))
  c = [(x + y) % mod for x, y in zip(a, b)]
  while c and c[-1] == 0:
    c.pop()
  return c

def Mod_S3(a):
  global n
  S = [1] * n
  a = RemainderDivision(a, S, 3)
  a = [x % 3 for x in a]
  a = [-1 if x == 2 else x for x in a]
  return a

def Mod_S2(a):
  global n
  S = [1] * n
  a = RemainderDivision(a, S, 2)
  a = [x % 2 for x in a]
  return a

def Mod_Rq(a):
  global n, q
  R = [0] * (n - 1) + [1]
  a = RemainderDivision(a, R, q)
  a = [x % q for x in a]
  a = [x - q if x > q / 2 - 1 else x for x in a]
  return a
