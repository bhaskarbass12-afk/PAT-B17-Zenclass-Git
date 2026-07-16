"""Vehicle Rental"""

from abc import ABC, abstractmethod


class Vehicle(ABC):
    """Base class for all vehicle types."""

    def __init__(self, model, rental_rate):
        self.model = model
        self.rental_rate = rental_rate  # base daily rental rate

    @abstractmethod
    def calculate_rental(self, days):
        """Calculate total rental cost. Must be implemented by subclasses."""
        pass

    def display_details(self, days):
        print(f"Model: {self.model}")
        print(f"Base Daily Rate: ₹{self.rental_rate}")
        print(f"Rental Duration: {days} days")
        print(f"Total Rental Cost: ₹{self.calculate_rental(days)}")
        print("-" * 40)


class Car(Vehicle):
    """Car with AC charge and fuel surcharge."""

    def __init__(self, model, rental_rate, ac_charge, fuel_surcharge):
        super().__init__(model, rental_rate)
        self.ac_charge = ac_charge          # daily AC charge
        self.fuel_surcharge = fuel_surcharge  # percentage (e.g., 10 for 10%)

    def calculate_rental(self, days):
        """Base rate + AC charge per day + fuel surcharge on total."""
        base_cost = (self.rental_rate + self.ac_charge) * days
        fuel_cost = base_cost * (self.fuel_surcharge / 100)
        return base_cost + fuel_cost


class Bike(Vehicle):
    """Bike with helmet charge and discount for long rentals."""

    def __init__(self, model, rental_rate, helmet_charge, long_rental_discount):
        super().__init__(model, rental_rate)
        self.helmet_charge = helmet_charge            # one-time helmet charge
        self.long_rental_discount = long_rental_discount  # percentage discount if days > 7

    def calculate_rental(self, days):
        """Base rate * days + helmet charge, with discount for 7+ days."""
        base_cost = self.rental_rate * days + self.helmet_charge
        if days > 7:
            discount = base_cost * (self.long_rental_discount / 100)
            base_cost -= discount
        return base_cost


class Truck(Vehicle):
    """Truck with load capacity charge and driver fee."""

    def __init__(self, model, rental_rate, load_capacity_tons, driver_fee_per_day):
        super().__init__(model, rental_rate)
        self.load_capacity_tons = load_capacity_tons  # capacity in tons
        self.driver_fee_per_day = driver_fee_per_day  # daily driver charge

    def calculate_rental(self, days):
        """Base rate + extra per ton of capacity + driver fee per day."""
        capacity_charge = self.load_capacity_tons * 200 * days  # ₹200 per ton per day
        driver_cost = self.driver_fee_per_day * days
        return (self.rental_rate * days) + capacity_charge + driver_cost


# --- Demonstrate polymorphism ---

if __name__ == "__main__":
    vehicles = [
        Car("Honda City", rental_rate=1500, ac_charge=200, fuel_surcharge=10),
        Bike("Royal Enfield", rental_rate=500, helmet_charge=100, long_rental_discount=15),
        Truck("Tata 407", rental_rate=3000, load_capacity_tons=5, driver_fee_per_day=800),
    ]

    rental_days = [5, 10, 3]  # different durations for each vehicle

    print("=" * 40)
    print("   VEHICLE RENTAL COST REPORT")
    print("=" * 40)

    for vehicle, days in zip(vehicles, rental_days):
        print(f"\nType: {type(vehicle).__name__}")
        vehicle.display_details(days)

    # Polymorphism — same method, different calculation per type
    print("\nTotal rental revenue: ₹", end="")
    total = sum(v.calculate_rental(d) for v, d in zip(vehicles, rental_days))
    print(total)