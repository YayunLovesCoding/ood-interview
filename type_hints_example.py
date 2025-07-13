"""
Example showing the difference between using and not using ABC and type hints
"""

# ============================================================================
# BAD APPROACH - Without ABC and type hints
# ============================================================================

class BadVehicle:
    def __init__(self, license_plate):
        self.license_plate = license_plate
    
    def get_size(self):
        # No clear contract - subclasses might forget to implement this
        pass

class BadCar(BadVehicle):
    # Oops! Forgot to implement get_size()
    pass

# This works but is wrong:
bad_car = BadCar("ABC123")
size = bad_car.get_size()  # Returns None - no error, but wrong!

# ============================================================================
# GOOD APPROACH - With ABC and type hints
# ============================================================================

from abc import ABC, abstractmethod
from typing import Optional, List
from enum import Enum

class VehicleSize(Enum):
    SMALL = "SMALL"
    MEDIUM = "MEDIUM"
    LARGE = "LARGE"

class GoodVehicle(ABC):
    def __init__(self, license_plate: str):
        self.license_plate = license_plate
    
    @abstractmethod
    def get_size(self) -> VehicleSize:
        """Must be implemented by subclasses"""
        pass

class GoodCar(GoodVehicle):
    def get_size(self) -> VehicleSize:
        return VehicleSize.MEDIUM

# This works correctly:
good_car = GoodCar("ABC123")
size = good_car.get_size()  # Returns VehicleSize.MEDIUM

# ============================================================================
# Type hints in action
# ============================================================================

def bad_function(vehicle):
    """Without type hints - unclear what this expects"""
    return vehicle.get_size()

def good_function(vehicle: GoodVehicle) -> VehicleSize:
    """With type hints - clear what goes in and comes out"""
    return vehicle.get_size()

# ============================================================================
# Optional in action
# ============================================================================

def bad_find_vehicle(vehicles, license_plate):
    """Without Optional - unclear what happens if not found"""
    for vehicle in vehicles:
        if vehicle.license_plate == license_plate:
            return vehicle
    return None  # What type is this? Unclear!

def good_find_vehicle(vehicles: List[GoodVehicle], license_plate: str) -> Optional[GoodVehicle]:
    """With Optional - clear that this might return None"""
    for vehicle in vehicles:
        if vehicle.license_plate == license_plate:
            return vehicle
    return None  # This is expected because of Optional

# ============================================================================
# Demonstration
# ============================================================================

def demonstrate_differences():
    print("=== Demonstrating ABC and Type Hints ===\n")
    
    print("1. Bad approach (without ABC):")
    try:
        bad_car = BadCar("ABC123")
        size = bad_car.get_size()
        print(f"   Bad car size: {size}")  # Prints None - wrong!
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n2. Good approach (with ABC):")
    try:
        good_car = GoodCar("ABC123")
        size = good_car.get_size()
        print(f"   Good car size: {size}")  # Prints VehicleSize.MEDIUM - correct!
    except Exception as e:
        print(f"   Error: {e}")
    
    print("\n3. Type hints help with function clarity:")
    vehicles = [GoodCar("CAR1"), GoodCar("CAR2")]
    
    # Without type hints - unclear what this returns
    result1 = bad_find_vehicle(vehicles, "CAR1")
    print(f"   Bad function result: {result1}")
    
    # With type hints - clear what this returns
    result2 = good_find_vehicle(vehicles, "CAR1")
    print(f"   Good function result: {result2}")
    
    print("\n4. What happens if we forget to implement abstract method?")
    try:
        class ForgotToImplement(GoodVehicle):
            pass  # Forgot to implement get_size()
        
        obj = ForgotToImplement("TEST")  # This will raise an error!
    except Exception as e:
        print(f"   Error caught: {e}")

if __name__ == "__main__":
    demonstrate_differences() 