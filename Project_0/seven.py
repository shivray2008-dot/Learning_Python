Number_Of_Years=int(input('Enter Number of Years: '))
Principal_Amount=int(input('Enter Principal Amount: '))
Rate_Of_Interest=int(input('Enter Rate Of Interest: %'))
Compound_Interest=Principal_Amount*(1+Rate_Of_Interest/100)**Number_Of_Years-Principal_Amount
if Number_Of_Years < 0 or Principal_Amount < 0 or Rate_Of_Interest < 0:
    print('Invalid Input')
if Number_Of_Years == 0:
    print('Compound Interest=0')
else:
    print(f'Compound Interest=${Compound_Interest:.2f}')