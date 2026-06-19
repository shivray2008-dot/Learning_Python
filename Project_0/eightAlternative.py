Cost_Of_Clothes=int(input('Enter Cost Of Clothes: $'))
if Cost_Of_Clothes <=1000:
    Discount=5/100
elif Cost_Of_Clothes <=2000:
    Discount=10/100
elif Cost_Of_Clothes <=3000:
    Discount=15/100

print(f'Discount = {Discount*100}%')
print('Final Price:', Cost_Of_Clothes-Cost_Of_Clothes*Discount)