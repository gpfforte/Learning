class Employee:
    def __init__(self, first, last, pay, *args):
        self.first = first
        self.last = last
        self.email = f"{first.lower()}.{last.lower()}@gmail.com"
        self.pay = pay
        if args:
            self.cell_number = args[0]

    def fullname(self):
        return f"{self.first} {self.last}"


emp_1 = Employee("Gianpietro", "Forte", 50000, 3351322874)
emp_2 = Employee("Test", "Employee", 60000)
print(emp_1.email)
print(emp_2.email)
print(f"Il nome è {emp_1.fullname()} e il numero di telefono è {emp_1.cell_number}")

