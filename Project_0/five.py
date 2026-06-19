# A library charges a fine for books returned late as given below:
# First five days ₹1 per day
# Six to ten days ₹2 per day
# Above ten days  ₹3 per day
# Design a program in Python (with relevant supporting material) to calculate the fine assuming that a book is returned N days late.
Number_Of_Units=int(input('Enter Number of Units: '))
if Number_Of_Units <=100 :
    fine=Number_Of_Units*1
elif Number_Of_Units <=200 :
    fine=(Number_Of_Units-100)*2+100
else:
    fine=(Number_Of_Units-200)*3+200
print(f'fine=\u20b9{fine}')