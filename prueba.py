import numpy as np

a=[1,2,3]
b=np.array(a)
d="hola"
c=np.where(b<5,b,[1,2,3])
print(c)