
import random
import datetime

class Employee:

    raise_amount = 1.04
    num_of_emps = 0
    
    def __init__(self, first, last, pay):
        self.emp_id = random.randint(1, 100000)
        self.first = first
        self.last= last
        self.pay =pay
        Employee.num_of_emps += 1
    
    # you make the employee id immutable and read only
    @property
    def emp_id(self):
        return self.emp_id
    
    @property
    def email(self):
        return self.first + '.' + self.last + '@company.com' 
    
    @property    
    def fullname(self):
        return '{} {}'.format(self.first, self.last)
    
    @fullname.setter
    def fullname(self, name):
        first, last = name.split(' ')
        self.first = first
        self.last = last
   
    @fullname.deleter
    def fullname(self):
        self.first = None
        self.last = None
        
    def apply_raise(self):
        self.pay = int(self.pay * self.raise_amount)
    
    @classmethod
    def set_raise_amt(cls, amount: 'int'):
        cls.raise_amount = amount
        
    #effecfively this is an ALTERNATIVE constructor
    @classmethod
    def from_string(cls, emp_str: 'str'):
        first, last, pay = emp_str.split('_')
        return cls(first, last, pay)
  
    @staticmethod
    def is_workday(day):
        if day.weekday() == 5 or day.weekday() == 6:
            return False
        return True
    
    def __repr__(self):
        return "Employee('{}', '{}', '{}')".format(self.first, self.last, self.pay)
    
    def __str__(self):
        pass

    def __add__(self, other: 'Employee'):
        return self.pay + other.pay
    
class Developer(Employee):
    def __init__(self, first, last, pay, prog_lang):
        super().__init__(first, last, pay)
        self.prog_lang = prog_lang
        
    raise_amount = 1.1

class Manager(Employee):
    def __init__(self, first, last, pay, employees=None):
        super().__init__(first, last, pay)
        if employees is None:
            self.employees = []
        else:
            self.employees = employees
    
    def add_employee(self, emp):
        if emp not in self.employees:
            self.employees.append(emp)
    
    def remove_employee(self, emp):
        if emp  in self.employees:
            self.employees.remove(emp) 
            
    def print_emps(self):
        for emp in self.employees:
            print(emp.fullname())
            
    def fullname(self):
        return '{} {} - {}'.format("Mr", self.first, self.last)
    
    raise_amount = 1.1

emp_str1 = 'Developer_Liyanawaduge_40000';
emp_str2 = 'Basilu_Liyanawaduge_80000';
emp_str3 = 'Devsith_Liyanawaduge_460000';
emp_str4 = 'Oliva_Rodirigo_750000';
first, last, pay = emp_str1.split('_')
new_emp1 = Developer(first, last, pay, 'python')
new_emp2 = Employee.from_string(emp_str2)
emp_1 = Developer('Developer', 'Nirosh', 50000, 'Java') 
emp_2 = Employee('Champika', 'Nirosh', 60000) 
emp_2.raise_amount = 1.02
Employee.set_raise_amt(1.06)
current_day = datetime.date(2024, 9, 10)
mgr_1 = Manager('marcus', 'fendnado', 70000, [emp_1, emp_2])
print(emp_1.fullname)
del emp_1.fullname
print(emp_1.fullname)
emp_1.fullname = "Devisith Damviru"
print(emp_1.fullname)

