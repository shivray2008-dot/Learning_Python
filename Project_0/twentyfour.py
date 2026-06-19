# Write a program to display the first N terms of the series:
# (b) 2, 5, 10, 17,…
x=1
n=int(input('Enter the number of terms: '))
while x<=n:
    print(x**2+1,end=" ")
    x+=1

