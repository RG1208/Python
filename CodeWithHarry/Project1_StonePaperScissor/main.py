"""
Stone paper scissor game
"""

import random
print("Welcome to Stone Paper Scissor Game")
print("\n")
computer_choice = random.choice(['stone', 'paper', 'scissor'])
user_choice = input("Enter your Choice: ").lower()

if (computer_choice==user_choice):
    print("Its a Draw")
else:
    if (computer_choice=='stone' and user_choice=='scissor') or \
       (computer_choice=='scissor' and user_choice=='paper') or \
       (computer_choice=='paper' and user_choice=='stone'):
        print("Computer Wins")
    else:
        print("User Wins")