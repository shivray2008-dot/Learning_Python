Name=str(input('Enter Customer name:'))
First_Meter_Reading=int(input('e:'))
Second_Meter_Reading=int(input('e2:'))
if Second_Meter_Reading < First_Meter_Reading:
    print('Meter Reading is not correct')
    exit()
Cost_Per_Unit=int(input('c:'))
q=Second_Meter_Reading-First_Meter_Reading
r=q*Cost_Per_Unit
print(f'Units_Consumed:{q}Watts')
print(f'Total_Cost:${r}')
if r>=600 :
    print('It is expensive')
else:
    print('It is affordable')