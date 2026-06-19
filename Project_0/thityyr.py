# 54321
# 5432
# 543
# 54
# 5
n=int(input('Enter the number of rows: '))
for i in range(n):
    for j in range(n,i,-1):
        print(j,end=' ')
    print()