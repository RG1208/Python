import random
n = random.randint(1, 100)
a=-1
guess=0
while a!=n:
    guess+=1
    a=int(input("Enter your guess: "))
    if a<n:
        print("Enter Higher number")
    else:
        print("Enter Lower number")

print(f"Congratulations! You guessed the correct number {n} in {guess} attempts.")