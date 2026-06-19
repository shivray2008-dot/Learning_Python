def are_coprime(a, b):
    """Check if two numbers are coprime using while loop"""
    # Get absolute values
    a = abs(a)
    b = abs(b)
    
    # Find GCD using Euclidean algorithm with while loop
    while b != 0:
        temp = b
        b = a % b
        a = temp
    
    # Two numbers are coprime if their GCD is 1
    return a == 1


# Test the function
num1 = int(input("Enter first number: "))
num2 = int(input("Enter second number: "))

if are_coprime(num1, num2):
    print(f"{num1} and {num2} are coprime")
else:
    print(f"{num1} and {num2} are not coprime")

