"""
Parking Lot System - Python Implementation
=========================================

This demonstrates Object-Oriented Design principles:
1. Encapsulation: Data and methods together
2. Inheritance: Vehicle types inherit from base Vehicle
3. Polymorphism: Different vehicles can be treated uniformly
4. Abstraction: Hide complex implementation details
5. Strategy Pattern: Different fare calculation strategies
6. Factory Pattern: Creating different parking spot types
"""

from abc import ABC, abstractmethod
from datetime import datetime
from enum import Enum
from typing import Optional, List, Dict
from decimal import Decimal
import uuid


# ============================================================================
# STEP 1: Define Core Enums and Constants
# ============================================================================

class VehicleSize(Enum):
    """Enum for vehicle sizes - helps with spot allocation"""
    SMALL = "SMALL"      # Motorcycles
    MEDIUM = "MEDIUM"    # Cars
    LARGE = "LARGE"      # Trucks


# ============================================================================
# STEP 2: Define Abstract Base Classes (Abstraction)
# ============================================================================

class Vehicle(ABC):
    """
    Abstract base class for all vehicles
    This demonstrates ABSTRACTION - we define what a vehicle should have
    without worrying about specific implementation details
    """
    
    def __init__(self, license_plate: str):
        self.license_plate = license_plate
    
    @abstractmethod
    def get_size(self) -> VehicleSize:
        """Each vehicle type must define its size"""
        pass
    
    def __str__(self):
        return f"{self.__class__.__name__}({self.license_plate})"


class ParkingSpot(ABC):
    """
    Abstract base class for parking spots
    Demonstrates ABSTRACTION - defines interface without implementation
    """
    
    def __init__(self, spot_number: int):
        self.spot_number = spot_number
        self.occupied_vehicle: Optional[Vehicle] = None
    
    @abstractmethod
    def get_size(self) -> VehicleSize:
        """Each spot type must define what size vehicles it can accommodate"""
        pass
    
    def is_available(self) -> bool:
        """Check if spot is available"""
        return self.occupied_vehicle is None
    
    def occupy(self, vehicle: Vehicle) -> bool:
        """
        Try to occupy spot with vehicle
        Returns True if successful, False if spot is already occupied
        """
        if self.is_available() and self.can_accommodate(vehicle):
            self.occupied_vehicle = vehicle
            return True
        return False
    
    def vacate(self) -> Optional[Vehicle]:
        """Remove vehicle from spot and return the vehicle"""
        vehicle = self.occupied_vehicle
        self.occupied_vehicle = None
        return vehicle
    
    def can_accommodate(self, vehicle: Vehicle) -> bool:
        """Check if this spot can accommodate the given vehicle"""
        return vehicle.get_size().value <= self.get_size().value
    
    def __str__(self):
        status = "Available" if self.is_available() else f"Occupied by {self.occupied_vehicle}"
        return f"Spot {self.spot_number} ({self.get_size().value}) - {status}"


class FareStrategy(ABC):
    """
    Abstract base class for fare calculation strategies
    This is the STRATEGY PATTERN - allows different pricing models
    """
    
    @abstractmethod
    def calculate_fare(self, ticket: 'Ticket', base_fare: Decimal) -> Decimal:
        """Calculate fare based on the strategy"""
        pass


# ============================================================================
# STEP 3: Implement Concrete Classes (Inheritance & Polymorphism)
# ============================================================================

class Car(Vehicle):
    """Concrete implementation of Vehicle for cars"""
    
    def get_size(self) -> VehicleSize:
        return VehicleSize.MEDIUM


class Motorcycle(Vehicle):
    """Concrete implementation of Vehicle for motorcycles"""
    
    def get_size(self) -> VehicleSize:
        return VehicleSize.SMALL


class Truck(Vehicle):
    """Concrete implementation of Vehicle for trucks"""
    
    def get_size(self) -> VehicleSize:
        return VehicleSize.LARGE


class RegularSpot(ParkingSpot):
    """Concrete implementation for regular parking spots"""
    
    def get_size(self) -> VehicleSize:
        return VehicleSize.MEDIUM


class CompactSpot(ParkingSpot):
    """Concrete implementation for compact parking spots"""
    
    def get_size(self) -> VehicleSize:
        return VehicleSize.SMALL
    
    def can_accommodate(self, vehicle: Vehicle) -> bool:
        """Compact spots can only accommodate small vehicles"""
        return vehicle.get_size() == VehicleSize.SMALL


class OversizedSpot(ParkingSpot):
    """Concrete implementation for oversized parking spots"""
    
    def get_size(self) -> VehicleSize:
        return VehicleSize.LARGE


class HandicappedSpot(ParkingSpot):
    """Concrete implementation for handicapped parking spots"""
    
    def get_size(self) -> VehicleSize:
        return VehicleSize.MEDIUM


# ============================================================================
# STEP 4: Implement Strategy Pattern for Fare Calculation
# ============================================================================

class BaseFareStrategy(FareStrategy):
    """
    Basic fare calculation strategy
    Demonstrates STRATEGY PATTERN - one way to calculate fares
    """
    
    def calculate_fare(self, ticket: 'Ticket', base_fare: Decimal) -> Decimal:
        """Simple fare calculation based on time"""
        duration = ticket.get_duration()
        hours = duration.total_seconds() / 3600
        return base_fare * Decimal(str(hours))


class PeakHoursFareStrategy(FareStrategy):
    """
    Peak hours fare calculation strategy
    Demonstrates STRATEGY PATTERN - different pricing during peak hours
    """
    
    def __init__(self, peak_multiplier: float = 1.5):
        self.peak_multiplier = Decimal(str(peak_multiplier))
    
    def calculate_fare(self, ticket: 'Ticket', base_fare: Decimal) -> Decimal:
        """Calculate fare with peak hours multiplier"""
        base_strategy = BaseFareStrategy()
        base_fare_amount = base_strategy.calculate_fare(ticket, base_fare)
        
        # Apply peak multiplier if during peak hours (simplified logic)
        entry_hour = ticket.entry_time.hour
        if 8 <= entry_hour <= 18:  # Peak hours: 8 AM to 6 PM
            return base_fare_amount * self.peak_multiplier
        return base_fare_amount


# ============================================================================
# STEP 5: Implement Core Business Logic Classes
# ============================================================================

class Ticket:
    """
    Represents a parking ticket
    Demonstrates ENCAPSULATION - data and related methods together
    """
    
    def __init__(self, ticket_id: str, vehicle: Vehicle, spot: ParkingSpot, entry_time: datetime):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = entry_time
        self.exit_time: Optional[datetime] = None
    
    def set_exit_time(self, exit_time: datetime):
        """Set the exit time when vehicle leaves"""
        self.exit_time = exit_time
    
    def get_duration(self) -> datetime:
        """Calculate parking duration"""
        if self.exit_time is None:
            raise ValueError("Vehicle hasn't left yet")
        return self.exit_time - self.entry_time
    
    def __str__(self):
        return f"Ticket {self.ticket_id} - {self.vehicle} at {self.spot}"


class ParkingManager:
    """
    Manages parking spots and vehicle assignments
    Demonstrates SINGLE RESPONSIBILITY PRINCIPLE - only handles parking logic
    """
    
    def __init__(self):
        self.spots: List[ParkingSpot] = []
        self.vehicle_to_spot: Dict[Vehicle, ParkingSpot] = {}
    
    def add_spot(self, spot: ParkingSpot):
        """Add a parking spot to the lot"""
        self.spots.append(spot)
    
    def park_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """
        Find an available spot for the vehicle and park it
        Returns the spot if successful, None if no spot available
        """
        # Find the best available spot for this vehicle
        for spot in self.spots:
            if spot.is_available() and spot.can_accommodate(vehicle):
                if spot.occupy(vehicle):
                    self.vehicle_to_spot[vehicle] = spot
                    return spot
        return None
    
    def unpark_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """
        Remove vehicle from its spot
        Returns the spot that was vacated
        """
        spot = self.vehicle_to_spot.get(vehicle)
        if spot and not spot.is_available():
            spot.vacate()
            del self.vehicle_to_spot[vehicle]
            return spot
        return None
    
    def find_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Find where a vehicle is parked"""
        return self.vehicle_to_spot.get(vehicle)
    
    def get_available_spots(self) -> List[ParkingSpot]:
        """Get list of available spots"""
        return [spot for spot in self.spots if spot.is_available()]


class FareCalculator:
    """
    Calculates parking fares using different strategies
    Demonstrates STRATEGY PATTERN - can use different pricing strategies
    """
    
    def __init__(self, strategy: FareStrategy, base_fare: Decimal = Decimal('5.00')):
        self.strategy = strategy
        self.base_fare = base_fare
    
    def calculate_fare(self, ticket: Ticket) -> Decimal:
        """Calculate fare using the configured strategy"""
        return self.strategy.calculate_fare(ticket, self.base_fare)


# ============================================================================
# STEP 6: Implement Main Parking Lot Class
# ============================================================================

class ParkingLot:
    """
    Main parking lot class that orchestrates all operations
    Demonstrates COMPOSITION - uses other classes to provide functionality
    """
    
    def __init__(self, parking_manager: ParkingManager, fare_calculator: FareCalculator):
        self.parking_manager = parking_manager
        self.fare_calculator = fare_calculator
    
    def enter_vehicle(self, vehicle: Vehicle) -> Optional[Ticket]:
        """
        Handle vehicle entry into parking lot
        Returns ticket if successful, None if no spot available
        """
        spot = self.parking_manager.park_vehicle(vehicle)
        if spot:
            ticket_id = f"TICKET-{uuid.uuid4().hex[:8].upper()}"
            ticket = Ticket(ticket_id, vehicle, spot, datetime.now())
            return ticket
        return None
    
    def leave_vehicle(self, ticket: Ticket) -> Optional[Decimal]:
        """
        Handle vehicle exit from parking lot
        Returns fare amount if successful, None if ticket is invalid
        """
        if ticket.exit_time is not None:
            return None  # Vehicle already left
        
        # Set exit time
        ticket.set_exit_time(datetime.now())
        
        # Remove vehicle from spot
        self.parking_manager.unpark_vehicle(ticket.vehicle)
        
        # Calculate and return fare
        fare = self.fare_calculator.calculate_fare(ticket)
        return fare
    
    def find_vehicle(self, vehicle: Vehicle) -> Optional[ParkingSpot]:
        """Find where a vehicle is parked"""
        return self.parking_manager.find_vehicle(vehicle)


# ============================================================================
# STEP 7: Factory Pattern for Creating Objects
# ============================================================================

class ParkingSpotFactory:
    """
    Factory for creating different types of parking spots
    Demonstrates FACTORY PATTERN - centralizes object creation
    """
    
    @staticmethod
    def create_spot(spot_type: str, spot_number: int) -> ParkingSpot:
        """Create a parking spot of the specified type"""
        if spot_type == "regular":
            return RegularSpot(spot_number)
        elif spot_type == "compact":
            return CompactSpot(spot_number)
        elif spot_type == "oversized":
            return OversizedSpot(spot_number)
        elif spot_type == "handicapped":
            return HandicappedSpot(spot_number)
        else:
            raise ValueError(f"Unknown spot type: {spot_type}")


# ============================================================================
# STEP 8: Example Usage and Testing
# ============================================================================

def create_sample_parking_lot() -> ParkingLot:
    """Create a sample parking lot with various spot types"""
    # Create parking manager
    parking_manager = ParkingManager()
    
    # Add different types of spots
    spot_number = 1
    for spot_type in ["compact", "regular", "regular", "handicapped", "oversized"]:
        spot = ParkingSpotFactory.create_spot(spot_type, spot_number)
        parking_manager.add_spot(spot)
        spot_number += 1
    
    # Create fare calculator with base strategy
    fare_calculator = FareCalculator(BaseFareStrategy())
    
    # Create parking lot
    return ParkingLot(parking_manager, fare_calculator)


def test_parking_lot():
    """Test the parking lot system"""
    print("=== Parking Lot System Test ===\n")
    
    # Create parking lot
    parking_lot = create_sample_parking_lot()
    
    # Create vehicles
    car = Car("ABC123")
    motorcycle = Motorcycle("XYZ789")
    truck = Truck("TRK456")
    
    print("1. Vehicle Entry:")
    print(f"   Car {car} entering...")
    ticket1 = parking_lot.enter_vehicle(car)
    if ticket1:
        print(f"   ✓ {ticket1}")
    else:
        print("   ✗ No spot available")
    
    print(f"\n   Motorcycle {motorcycle} entering...")
    ticket2 = parking_lot.enter_vehicle(motorcycle)
    if ticket2:
        print(f"   ✓ {ticket2}")
    else:
        print("   ✗ No spot available")
    
    print(f"\n   Truck {truck} entering...")
    ticket3 = parking_lot.enter_vehicle(truck)
    if ticket3:
        print(f"   ✓ {ticket3}")
    else:
        print("   ✗ No spot available")
    
    print("\n2. Vehicle Exit:")
    if ticket1:
        print(f"   Car {car} leaving...")
        fare = parking_lot.leave_vehicle(ticket1)
        if fare:
            print(f"   ✓ Fare: ${fare:.2f}")
    
    print("\n3. Current Status:")
    for spot in parking_lot.parking_manager.spots:
        print(f"   {spot}")


if __name__ == "__main__":
    test_parking_lot() 