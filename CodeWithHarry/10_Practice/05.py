from random import randint

class TrainDetails:

    def __init__(self,trainNo):
        self.trainNo = trainNo

    def book(self, fro, to):
        print(f"Booking confirmed from {fro} to {to} on train number {self.trainNo}.")
    
    def get_status(self, fro,to):
        status = randint(0, 1)
        if status:
            print(f"Train number {self.trainNo} from {fro} to {to} is on time.")
        else:
            print(f"Train number {self.trainNo} from {fro} to {to} is delayed.")

    def fair(self, fro, to):
        fair_amount = randint(100, 500)
        print(f"The fare from {fro} to {to} on train number {self.trainNo} is ${fair_amount}.")

train1 = TrainDetails(101)
train1.book("New York", "Washington D.C.")
train1.get_status("New York", "Washington D.C.")
train1.fair("New York", "Washington D.C.")