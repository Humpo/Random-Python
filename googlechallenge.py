def isprime(n):
    n = abs(int(n))
    if n < 2:return (False)
    if n == 2:return (True)    
    if not n & 1: return (False)
    for x in range(3, int(n**0.5)+1, 2):
        if n % x == 0:return (False)
    return (True)
def z(contfrac, a=1, b=0, c=0, d=1):
    for x in contfrac:
        while a > 0 and b > 0 and c > 0 and d > 0:
            t = a // c
            t2 = b // d
            if not t == t2:
                break
            yield (t)
            a = (10 * (a - c*t))
            b = (10 * (b - d*t))
            # continue with same fraction, don't pull new x
        a, b = x*a+b, a
        c, d = x*c+d, c
    for digit in rdigits(a, c):
        yield (digit)
def rdigits(p, q):
    while p > 0:
        if p > q:
           d = p // q
           p = p - q * d
        else:
           d = (10 * p) // q
           p = 10 * p - q * d
        yield (d)
def e_cf_expansion():
    yield (1)
    k = 0
    while True:
        yield (k)
        k += 2
        yield (1)
        yield (1)
def e_dec():return z(e_cf_expansion())
def e_gen(n):
    gen = e_dec()
    e = [str(next(gen)) for i in range(n)]
    #e.insert(1, '.')#inserting decimal
    return(''.join(e))
#window loop
for location in range(1000):
    num = int(e_gen(10000)[location:(10+location)])
    val = isprime(num)
    if  val== True:
        print (num)
        break
#from google challenge in 2007 for a job at google
#{first 10-digit prime found in consecutive digits of e}.com
