from math import log
import random

def getModular(x):
    result = 0
    for i in range(32):
        if x[i] == 'n':
            result += pow(2, 31-i)
        elif x[i] == "u":
            result -= pow(2, 31 - i)
    return result & 0xffffffff

def leftRotate_str(lst, s):
    return lst[s:] + lst[:s]

def leftRotate(n, s):
    return (n << s) | (n >> (32 - s))

# step-44
# X40 <<< 10 + Y39 <<< 10 = 0
# X41 <<< 10 + Y40 <<< 10 = 0
# X42 + Y41 <<< 10 = 0

# X40/X41/X42
X = ["===111=0======n==0===1====11====",
"===n0=00======1===============0=",
"===1==nn======================n="]

# Y39/Y40/Y41
Y = ["===0====1=====u===========1====1",
"===u====0=====1=10==============",
"===1====u=======uu===0=========0"]


MX = []
sx = [10, 10, 0]
for i in range(len(X)):
    MX.append(getModular(leftRotate_str(X[i], sx[i])))

MY = []
sy = [10, 10, 10]
for i in range(len(Y)):
    MY.append(getModular(Y[i]))

print(MX)
proList = []
totalData = pow(2, 24)

for i in range(len(Y)):
    num = 0
    for j in range(totalData):
        y0 = random.randint(0, pow(2,32)) & 0xffffffff
        y1 = (y0 + MY[i]) & 0xffffffff

        yModular = (leftRotate(y1, sy[i]) - leftRotate(y0, sy[i])) & 0xffffffff

        if ((MX[i] + yModular) & 0xffffffff) == 0:
            num += 1
    # print(num)
    print("step probability:", log(num / totalData, 2))
    proList.append(log(num / totalData, 2))
    print()

print("total probability:", sum(proList))
