n=int(input('Enter a random number: '))
if n<=1:
    print('The number is not prime')
else:
    for i in range(2,n):
        if n%i==0:
            print('the number is not prime')
        else:
            print('The number is prime')