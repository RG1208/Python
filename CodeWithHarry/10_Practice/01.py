class Employee():
    company="microsoft"
    def __init__(self, name, position, salary):
        self.name = name
        self.position = position
        self.salary = salary


p = Employee("Alice", "Developer", 70000)
print(p.name, p.position, p.salary)