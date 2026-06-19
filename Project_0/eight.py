Cost_Of_Clothes=int(input('Enter Cost Of Clothes: $'))
if Cost_Of_Clothes <=1000:
    print('Discount=5%')
elif Cost_Of_Clothes >1000 and Cost_Of_Clothes <=2000:
    print('Discount=10%')
elif Cost_Of_Clothes >2000 and Cost_Of_Clothes <=3000:
    print('Discount=15%')

if Cost_Of_Clothes <=1000:
   print('Final Price:', Cost_Of_Clothes-Cost_Of_Clothes*5/100)
elif Cost_Of_Clothes >1000 and Cost_Of_Clothes <=2000:
    print('Final Price:', Cost_Of_Clothes-Cost_Of_Clothes*10/100)
elif Cost_Of_Clothes >2000 and Cost_Of_Clothes <=3000:
    print('Final Price:', Cost_Of_Clothes-Cost_Of_Clothes*15/100)