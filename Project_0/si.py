Physics=int(input('Enter the Physics Marks:'))
Chemistry=int(input('Enter the Chemistry Marks:'))
Maths=int(input('Enter the Maths Marks:'))
Biology=int(input('Enter the Biology Marks:'))
ComputerScience=int(input('Enter the Computer Science Marks:'))
Percentage=(Physics+Chemistry+Maths+Biology+ComputerScience)/5
print(f'Percentage={Percentage}%')
if Percentage >=90:
    print('Grade A')
elif Percentage >=75:
    print('Grade B')
else:
    print('Grade C')
if Percentage >100 or Percentage <0:
    print('Invalid Percentage')