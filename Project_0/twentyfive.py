# Write a program to display the first N terms of the series:
# (b) 2, 5, 10, 17,…
x=1
d=1
t=1
n=int(input('Enter the number of terms: '))
while x<=n:
    t=t+d
    print(t,end=" ")
    x+=1
    d+=2
