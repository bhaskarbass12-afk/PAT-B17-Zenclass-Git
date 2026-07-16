"""Employee management"""

from abc import ABC, abstractmethod

class Employee(ABC):
    """Base class for all employee types."""

    def __init__(self, name, salary):
        self.name = name
        self.salary = salary

    @abstractmethod
    def calculate_salary(self):
        """Calculate the total salary. Must be implemented by subclasses."""
        pass

    def display_details(self):
        print(f"Name: {self.name}")
        print(f"Base Salary: {self.salary}")
        print(f"Total Salary: {self.calculate_salary()}")
        print("-" * 40)


class RegularEmployee(Employee):
    """Regular full-time employee with benefits and bonus."""

    def __init__(self, name, salary, bonus, benefits):
        super().__init__(name, salary)
        self.bonus = bonus        # annual bonus percentage (e.g., 10 for 10%)
        self.benefits = benefits  # fixed monthly benefits amount

    def calculate_salary(self):
        """Salary + bonus percentage + benefits."""
        bonus_amount = self.salary * (self.bonus / 100)
        return self.salary + bonus_amount + self.benefits


class ContractEmployee(Employee):
    """Contract employee paid by hours worked."""

    def __init__(self, name, salary, hourly_rate, hours_worked):
        super().__init__(name, salary)
        self.hourly_rate = hourly_rate
        self.hours_worked = hours_worked

    def calculate_salary(self):
        """Paid based on hourly rate and hours worked."""
        return self.hourly_rate * self.hours_worked


class Manager(Employee):
    """Manager with bonus, benefits, and team leadership allowance."""

    def __init__(self, name, salary, bonus, benefits, team_size):
        super().__init__(name, salary)
        self.bonus = bonus        # annual bonus percentage
        self.benefits = benefits  # fixed monthly benefits amount
        self.team_size = team_size  # number of people managed

    def calculate_salary(self):
        """Salary + bonus + benefits + leadership allowance per team member."""
        bonus_amount = self.salary * (self.bonus / 100)
        leadership_allowance = self.team_size * 500  # 500 per team member
        return self.salary + bonus_amount + self.benefits + leadership_allowance


# --- Demonstrate polymorphism ---

if __name__ == "__main__":
    employees = [
        RegularEmployee("Alice", 50000, bonus=10, benefits=5000),
        ContractEmployee("Bob", 0, hourly_rate=150, hours_worked=160),
        Manager("Charlie", 80000, bonus=15, benefits=8000, team_size=6),
    ]

    print("=" * 40)
    print("   EMPLOYEE SALARY REPORT")
    print("=" * 40)

    for emp in employees:
        print(f"\nType: {type(emp).__name__}")
        emp.display_details()

    # Polymorphism in action — same method call, different behavior
    print("\nTotal payroll:", sum(emp.calculate_salary() for emp in employees))