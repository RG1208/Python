class User:
    def add(self,n):
        self.n=n
        print(self.n + 5)
    
    @staticmethod
    def greet():
        print("Hello, welcome to the User class!")
    
user1 = User()
user1.add(10)
user1.greet()