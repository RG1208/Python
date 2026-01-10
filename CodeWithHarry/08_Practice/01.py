def greatest(num1,num2,num3):
    if (num1>num2 and num1>num3):
        print(f"{num1} is greatest")
    elif(num2>num1 and num2>num3):
        print(f"{num2} is greatest")
    else:
        print(f"{num3} is greatest")

greatest(1,2,3)
greatest(88,100,2)
greatest(99,4,27)
