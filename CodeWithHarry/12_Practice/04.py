try:
    a = int(input("Enter a number: "))
    b = int(input("Enter b number: "))
    division = a/b
    print("The result is:",division)
except ZeroDivisionError as e:
    print("Division by 0 not possible")