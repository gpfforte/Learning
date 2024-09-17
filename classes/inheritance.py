class Employee:
    raise_amt = 1.04

    def __init__(self, first, last, pay):
        self.first = first
        self.last = last
        self.email = f"{first.lower()}.{last.lower()}@gmail.com"
        self.pay = pay

    def fullname(self):
        return f"{self.first} {self.last}"

    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amt)

    def __str__(self) -> str:
        return f"Employeee {self.fullname()}"

    def __repr__(self) -> str:
        return f"Employeee({self.first}, {self.last}, {self.pay})"


class Developer(Employee):
    raise_amt = 1.10

    def __init__(self, first, last, pay, prog_lang=None):
        super().__init__(first, last, pay)
        if prog_lang is None:
            self.prog_lang = []
        else:
            self.prog_lang = prog_lang

    def add_lang(self, lang):
        if lang not in self.prog_lang:
            self.prog_lang.append(lang)

    def remove_emp(self, lang):
        if lang in self.prog_lang:
            self.prog_lang.remove(lang)

    def print_lang(self):
        print()
        print(f"{self.fullname()} conosce i seguenti linguaggi:")
        for lang in self.prog_lang:
            print(lang)
        print()

    def __str__(self) -> str:
        return f"Developer {self.fullname()}"

    def __repr__(self) -> str:
        return f"Developer({self.first}, {self.last}, {self.pay})"


class Manager(Employee):
    raise_amt = 1.08

    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees

    def add_emp(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)

    def remove_emp(self, emp):
        if emp in self.employees:
            self.employees.remove(emp)

    def print_emps(self):
        for emp in self.employees:
            # print("-->", emp.fullname())
            print(emp)

    def __str__(self) -> str:
        return f"Manager {self.fullname()}"

    def __repr__(self) -> str:
        return f"Manager({self.first}, {self.last}, {self.pay})"


emp1 = Employee("Gp", "F", 50000)
# print(emp1)

dev_1 = Developer("Corey", "Schafer", 50000, ["Python"])

dev_2 = Developer("Test", "Employee", 60000, ["Java"])
dev_2.add_lang("C++")
dev_2.print_lang()
# print(dev_1)
mgr_1 = Manager("Sue", "Smith", 90000, [dev_1, emp1])

# print(mgr_1)
# print(mgr_1.email)
print(mgr_1.raise_amt)

mgr_1.add_emp(dev_2)
# mgr_1.remove_emp(dev_2)
# print(mgr_1.employees)
# mgr_1.print_emps()

