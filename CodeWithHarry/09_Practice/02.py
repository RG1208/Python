import random

def game():
    choice= random.randint(1,10)
    return choice

computer_choice = game()

with open("hi-score.txt") as file:
    content = file.read()
    high_score = int(content)

if high_score>=computer_choice:
    print("you loose")
else:
    with open("hi-score.txt","w") as file:
        file.write(str(computer_choice))
        print("you win, hi score updated")