try:
    with open("01.txt","r") as f:
        a=f.read()
        print(a)
except FileNotFoundError:
    print("The file does not exist.")

try:
    with open("02.txt","r") as f:
        a=f.read()
        print(a)
except FileNotFoundError:
    print("The file does not exist.")

try:
    with open("03.txt","r") as f:
        a=f.read()
        print(a)
except FileNotFoundError:
    print("The file does not exist.")