# ALGORITMO DE EUCLIDES
def Euclides(a, b):
  if b == 0:
    return a
  else:
    return Euclides(b, a%b)

def Ext_Euclides(a, b):
  if b == 0:
    return (a, 1, 0)
  else:
    d, x_, y_ = Ext_Euclides(b, a%b)
    x, y = y_, x_ - int(a/b)*y_
    return (d, x, y)

def Inversa(a, n):
  if Euclides(a, n) == 1:
    mgd, x, y = Ext_Euclides(a, n)
    return x % n
  else:
    print("No existe")

# MILLER RABIN
import random

def EXPMOD(a, x, n):
  c = a % n
  r = 1
  while (x > 0):
    if x % 2 != 0:
      r = (r * c) % n
    c = (c * c) % n
    x = int(x/2)
  return r

def ES_COMPUESTO(a, n, t, u):
  x = EXPMOD(a,u,n)
  if x == 1 or x == n-1:
    return False  # n posiblemente primo
  for i in range(t):
    x = EXPMOD(x,2,n)
    if x == n-1:
      return False  # n posiblemente primo
  return True    # n es un número compuesto

def gen_random_a(n, s):  # genera "s" numeros random unicos en el rango de 2 y n-1, si no se pueden generar "s" números entonces retorna lo que tenga.
  randoms = []
  maximo = min(s, n-3)
  while len(randoms) < maximo:
    num = random.randint(2, n-1)
    if num not in randoms:
      randoms.append(num)
  return randoms

def MILLER_RABIN(n, s):
  t = 0
  u = n - 1
  while u % 2 == 0:
    u = u//2
    t = t + 1
  #for a in gen_random_a(n, s):
  for _ in range(s):
    a = random.randint(2, n-1)
    if ES_COMPUESTO(a, n, t, u):
      return False
  return True

def RANDOMBITS(b):
  n = random.randint(0, 2**b - 1)
  m = 2**(b-1) + 1
  return n | m    # el operador "|" nos permite hacer una operación binaria de "n" y "m"

def RANDOMGEN_PRIMOS(b, s):
  n = RANDOMBITS(b)
  while MILLER_RABIN(n, s) == False:
    n = n + 2
  return n

def GEN_PRIMO_SIGUIENTE(n, s):
  n = n + 1 - (n % 2)
  while MILLER_RABIN(n, s) == False:
    n = n + 2
  return n

# RSA KEY GENERATOR
class RSA:
  def __init__(self, k):
    n = 1
    while True:
      self.e, self.d, self.n = self.RSA_KEY_GENERATOR(k, 10**n)
      m = random.randint(2,self.n-1)
      c = self.Cifrado(m)
      if m == self.Descifrado(c):
        break
      else:
        n += 1

    print("RSA \n s={:}, e={:}, d={:}, n={:}, phi={:}".format(10**n, self.e, self.d, self.n, self.phi))

  def RSA_KEY_GENERATOR(self, k, s):
    if k<8:    # generar primos con bits menores al dividirlos entre 2 no abria muchos, ocurria un loop, o un error.
      k = 8
    p = RANDOMGEN_PRIMOS(k//2, s)
    q = RANDOMGEN_PRIMOS(k//2, s)
    while p==q:
      q = RANDOMGEN_PRIMOS(k//2, s)

    n, self.phi = p*q, (p-1)*(q-1)

    e = random.randint(2,n-1)
    while Euclides(e, self.phi)!=1:
      e = random.randint(2, n-1)
      
    d = Inversa(e, self.phi)
    return e, d, n

  def Cifrado(self, m):
    return EXPMOD(m, self.e, self.n)

  def Descifrado(self, c):
    return EXPMOD(c, self.d, self.n)
  
  def get_edn(self):
    return self.e, self.d, self.n

rsa = RSA(8)


rsa = RSA(48)

mensaje = 11
print("\nMensaje original: ", mensaje)
c = rsa.Cifrado(mensaje)
print("Cifrado: ", c)
print("Descifrado: ", rsa.Descifrado(c), "\n")


def Cifrado(msg):
  cade = ""
  data = []
  for m in msg:
    me = rsa.Cifrado(ord(m))    # pasamos el valor en ascci de la palabra a el Cifrado RSA
    encrip = me % ord('A') + 65   # rango [65, 122] donde 65='A' y 122='z'
    cade += str("%c" % encrip)   # convertimos de decimal a word ascci
    data.append(me)
  return cade, data

def Descifrado(msg, data):
  cade = ""
  for i in range(len(msg)):
    med = rsa.Descifrado(data[i])
    cade += str("%c" % med)
  return cade

words = ["Hello", "World", "Python", "CComp", "Algebra", "UCSP"]
for word in words:
  word_2, data = Cifrado(word)
  word_3 = Descifrado(word_2, data)
  print("Mnsje inicial = {:}, Cifrado = {:}, Descifrado = {:})".format(word, word_2, word_3))
