"""
Test file to demonstrate OOD principles and design patterns
"""

from parking_lot_python import *
from decimal import Decimal

def test_inheritance_and_polymorphism():
    """Test inheritance and polymorphism principles"""
    print("=== Testing Inheritance and Polymorphism ===\n")
    
    # Create different types of vehicles
    vehicles = [
        Car("CAR001"),
        Motorcycle("BIKE001"), 
        Truck("TRUCK001")
    ]
    
    print("1. Polymorphism in action:")
    for vehicle in vehicles:
        size = vehicle.get_size()
        print(f"   {vehicle}: {size.value}")
    
    print("\n2. All vehicles can be treated uniformly:")
    for vehicle in vehicles:
        print(f"   {vehicle} has license plate: {vehicle.license_plate}")


def test_strategy_pattern():
    """Test the strategy pattern for fare calculation"""
    print("\n=== Testing Strategy Pattern ===\n")
    
    # Create a sample ticket with entry and exit times
    car = Car("TEST001")
    spot = RegularSpot(1)
    entry_time = datetime.now()
    ticket = Ticket("TEST-TICKET", car, spot, entry_time)
    
    # Set exit time (simulating vehicle leaving)
    from datetime import timedelta
    ticket.set_exit_time(entry_time + timedelta(hours=2))  # 2 hours later
    
    # Test different fare strategies
    strategies = [
        ("Base Strategy", BaseFareStrategy()),
        ("Peak Hours Strategy", PeakHoursFareStrategy(1.5))
    ]
    
    print("1. Different fare calculation strategies:")
    for name, strategy in strategies:
        calculator = FareCalculator(strategy, Decimal('5.00'))
        fare = calculator.calculate_fare(ticket)
        print(f"   {name}: ${fare:.2f}")


def test_factory_pattern():
    """Test the factory pattern for creating parking spots"""
    print("\n=== Testing Factory Pattern ===\n")
    
    print("1. Creating different types of parking spots:")
    spot_types = ["compact", "regular", "oversized", "handicapped"]
    
    for i, spot_type in enumerate(spot_types, 1):
        spot = ParkingSpotFactory.create_spot(spot_type, i)
        print(f"   {spot_type.capitalize()} Spot: {spot}")


def test_encapsulation():
    """Test encapsulation principles"""
    print("\n=== Testing Encapsulation ===\n")
    
    # Create a ticket
    car = Car("ENCAP001")
    spot = RegularSpot(1)
    ticket = Ticket("ENCAP-TICKET", car, spot, datetime.now())
    
    print("1. Ticket data is encapsulated:")
    print(f"   Ticket ID: {ticket.ticket_id}")
    print(f"   Vehicle: {ticket.vehicle}")
    print(f"   Spot: {ticket.spot}")
    print(f"   Entry Time: {ticket.entry_time}")
    
    print("\n2. Duration calculation is encapsulated:")
    try:
        duration = ticket.get_duration()
        print(f"   Duration: {duration}")
    except ValueError as e:
        print(f"   Error: {e}")


def test_single_responsibility():
    """Test single responsibility principle"""
    print("\n=== Testing Single Responsibility ===\n")
    
    # Create components with single responsibilities
    parking_manager = ParkingManager()
    fare_calculator = FareCalculator(BaseFareStrategy())
    
    print("1. ParkingManager only handles parking:")
    print(f"   Type: {type(parking_manager).__name__}")
    print(f"   Methods: {[method for method in dir(parking_manager) if not method.startswith('_')]}")
    
    print("\n2. FareCalculator only handles fare calculation:")
    print(f"   Type: {type(fare_calculator).__name__}")
    print(f"   Methods: {[method for method in dir(fare_calculator) if not method.startswith('_')]}")


def test_composition():
    """Test composition over inheritance"""
    print("\n=== Testing Composition ===\n")
    
    # Create parking lot using composition
    parking_manager = ParkingManager()
    fare_calculator = FareCalculator(BaseFareStrategy())
    parking_lot = ParkingLot(parking_manager, fare_calculator)
    
    print("1. ParkingLot is composed of:")
    print(f"   ParkingManager: {type(parking_lot.parking_manager).__name__}")
    print(f"   FareCalculator: {type(parking_lot.fare_calculator).__name__}")
    
    print("\n2. We can easily swap components:")
    peak_calculator = FareCalculator(PeakHoursFareStrategy())
    new_parking_lot = ParkingLot(parking_manager, peak_calculator)
    print(f"   New calculator type: {type(new_parking_lot.fare_calculator).__name__}")


def test_abstraction():
    """Test abstraction principles"""
    print("\n=== Testing Abstraction ===\n")
    
    print("1. Vehicle abstraction:")
    print("   - We don't need to know how Car, Motorcycle, Truck work internally")
    print("   - We just know they all have get_size() method")
    
    print("\n2. ParkingSpot abstraction:")
    print("   - We don't need to know how RegularSpot, CompactSpot work internally")
    print("   - We just know they all have is_available() and occupy() methods")
    
    print("\n3. FareStrategy abstraction:")
    print("   - We don't need to know how BaseFareStrategy, PeakHoursFareStrategy work")
    print("   - We just know they all have calculate_fare() method")


if __name__ == "__main__":
    print("OOD Principles and Design Patterns Demonstration\n")
    print("=" * 50)
    
    test_inheritance_and_polymorphism()
    test_strategy_pattern()
    test_factory_pattern()
    test_encapsulation()
    test_single_responsibility()
    test_composition()
    test_abstraction()
    
    print("\n" + "=" * 50)
    print("All tests completed! This demonstrates how OOD principles")
    print("make code more maintainable, extensible, and testable.") 