# Write a program to understand the colour of the symbol at the road crossing
Signal_Colour=str(input('Enter Signal Colour: '))
if Signal_Colour=="red" or  Signal_Colour=='RED':
    print('Stop Signal')
elif Signal_Colour=='orange' or Signal_Colour=='ORANGE':
    print('slow down Signal')
elif Signal_Colour=='green' or  Signal_Colour=='GREEN':
    print('GO Symbol')
else:
    print('INVALID')
