

import matplotlib.pyplot as plt

n = [i for i in range(-30,31)]
xn = []

ze = [0.6]
for i in range(len(n)):
    if n[i] == 0:
        new_d = n[:i+1] + ze + n[i+1:]

for i in new_d:
    if i%2 == 0:
        xn.append(1)
    elif i == 0.6:
        xn.append(2.690+0.951j)
    else :
        xn.append(0)

print(xn)


# print(new_d)


plt.figure()
plt.stem(new_d, xn)
plt.ylim(0,5)
plt.title('plot x[n] = u[(-1^n)] + 3δ[5n-3] and n')
plt.xlabel('n')
plt.ylabel('x[n]')
plt.savefig('aaaaaaa')
plt.show()
