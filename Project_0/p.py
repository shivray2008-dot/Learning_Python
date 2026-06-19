# 12345
# 2345
# 345
# 45
# 5
n=int(input('Enter the number of rows: '))
for i in range(n):
    for j in range(i+1,n+1):
        print(j,end=" ")
    print() 