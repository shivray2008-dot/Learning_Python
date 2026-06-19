# 5
# 5 4
# 5 4 3
# 5 4 3 2
# 5 4 3 2 1
n=int(input("Enter the number of terms: "))
for i in range(n+1,0,-1):
    for j in range(i-1,n):
        print(j,end=' ')
    print()