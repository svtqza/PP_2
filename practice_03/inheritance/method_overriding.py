#1
class Vehicle:
    def start_engine(self):
        print("Starting engine of the vehicle...")
class Car(Vehicle):
    def start_engine(self):
        print("Starting engine of the car... Vroom vroom!")
v = Vehicle()
v.start_engine() 
c = Car()
c.start_engine()  

#2

class Employee:
    def calculate_salary(self, hours_worked):
        return hours_worked * 20 
class Manager(Employee):
    def calculate_salary(self, hours_worked):
        base = super().calculate_salary(hours_worked) 
        bonus = 500  
        return base + bonus
e = Employee()
print(e.calculate_salary(40)) 
m = Manager()
print(m.calculate_salary(40))  

