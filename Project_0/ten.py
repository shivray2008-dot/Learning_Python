n=int(input('n='))
count=0
for i in range(3,n**4,6):
    if i%3==0 and i%2!=0:
        print(i,end=' ')
        count+=1
    if count ==n:
        break
if n==1:
    print('3')
    