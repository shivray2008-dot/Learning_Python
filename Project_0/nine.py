Parking_Time=int(input("Enter the parking time in hours: Hours "))
if Parking_Time <= 2:   
    print("Parking fee is $5")
elif Parking_Time > 2 and Parking_Time <= 5:
    print("Parking fee is $10")
elif Parking_Time > 5 and Parking_Time <= 10:
    print("Parking fee is $15")
elif Parking_Time > 10:
    print("Parking fee is $20")
if Parking_Time <=2:
    print('Total Parking Fee Each Hour: ${:.2f}'.format(Parking_Time*5) )
elif Parking_Time > 2 and Parking_Time <= 5:
    print('Total Parking Fee Each Hour: ${:.2f}'.format(Parking_Time*10) )
elif Parking_Time > 5 and Parking_Time <= 10:
    print('Total Parking Fee Each Hour: ${:.2f}'.format(Parking_Time*15)) 
elif Parking_Time > 10: 
    print('Total Parking Fee Each Hour: ${:.2f}'.format(Parking_Time*20) )
