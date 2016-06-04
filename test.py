__author__ = 'HyNguyen'

i = - 1000
while i < 0:
    if abs(i**5 + 2*(i**4) + 2*i  + 1) < 0.00001 :
        print i
    i+= 0.00001


