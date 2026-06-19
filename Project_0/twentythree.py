# Write a program to display the first N terms of the series:
# (a) 1,-3, 5, -7,9,…
x=1
sign=1
n=int(input('Enter number of terms : '))
while x<=n:
    print((x*2-1)*sign,end=" ")
    sign=sign*(-1)
    x+=1
    
