from netcat import Netcat
import re

# the function given by the server
def gg(tup, a, x):
    (p, g), n = tup, len(a)
    assert len(bin(x)[2:]) <= n
    X = bin(x)[2:].zfill(n)
    f_ax = g
    for i in range(1, n):
        f_ax *= pow(g, a[i] * int(X[i]), p)
    return f_ax % p

'''
Ok, this problem had a netcat interface and I wasn't very happy.
However, the PRF was short and easy to read; the first idea was to send some Xs with only one 1 and the rest 0s, in order to get a[i] by solving a discrete log.
The idea wasn't bad, but the server required the inputs to be at least 2^64; so I took the opposite approach and asked for Xs with all ones but one 0 in the needed.
The discrete log wasn't hard, because g always had an order of ~200.
'''


nc = Netcat('167.71.62.250', 23549)

# read PoW request
print(nc.read())

# send PoW
pwd = input("Inserisci la pass")
nc.write(pwd+'\n')

# read parameters
header = nc.read_until('[Q]uit')
print(header)
nums = re.findall(r"\(p, g\) = \((.*?), (.*?)\)", header)
N = int(re.findall(r"for n = (\d*)", header)[0])

p = int(nums[0][0], 16)
g = int(nums[0][1], 16)
print(p, g)


# compute a table of all powers of g, and its order
logs = {1: 0}

x = g
ord = 1
while (x != 1):
    logs[x] = ord
    x = x*g % p
    ord += 1

print(ord)


# actually get a: for every index ask for 2^i or 2^127-2^i-1, which are the one-hot or zero-hot encodings
a = [0]*128
b = [0]*128

pow127 = 2**127

for i in range(0,128):
    nc.write("N\n")
    nc.read_until("[N]o")

    nc.write("Y\n")
    nc.read()

    if (i<=64):
        c = pow127 - 2**i - 1
    else:
        c = 2**i

    nc.write(str(c)+"\n")
    res = str(nc.read_until('[Q]uit'))
    num = int(re.findall(r"f_a\(n \+ 0\) = (\d*)", res)[0])
    a[127-i] = logs[num] - 1
    b[i] = logs[num]
    print(i, num, logs[num])

# actually I needed an extra number
nc.write("N\n")
nc.read_until("[N]o")

nc.write("Y\n")
nc.read()

nc.write(str(pow127-2**65-1)+"\n")
res = str(nc.read_until('[Q]uit'))
num = int(re.findall(r"f_a\(n \+ 0\) = (\d*)", res)[0])
b[65] = logs[num]
print(b)

c = a[62]+b[65]
print(c)

# compute all a
for i in range(63,128):
    a[i] = c - b[127-i]

for i in range(128):
    if (a[i]<0):
        a[i] = a[i] + ord

print(a)

# various checks to see if a is right
print(hex(p), hex(g), N)
print(gg((p,g),a,N))

S = sum(a)
z = pow(g, 1+S, p)

print(logs[z], c%ord)

# send the number to solve the challenge
nc.write("N\n")
nc.read_until("[N]o")

nc.write("N\n")
new_res = str(nc.read_until('[Q]uit'))
print(new_res)
N = int(re.findall(r"for n = (\d*)", new_res)[0])

guess = gg((p,g),a,N+5)

nc.write("G\n")
print(nc.read())

nc.write(str(guess)+"\n")
print(nc.read())

# Yay, the flag!
