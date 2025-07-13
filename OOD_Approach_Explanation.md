# Object-Oriented Design Approach: Parking Lot System

## **High-Level Strategy for Tackling OOD Problems**

### **Step 1: Understand the Problem Domain**
Before writing any code, you need to understand:
- **What are the main entities?** (Vehicle, ParkingSpot, Ticket, etc.)
- **What are the core operations?** (Park, Unpark, Calculate Fare)
- **What are the relationships?** (Vehicle → ParkingSpot, Ticket → Vehicle)
- **What are the constraints?** (Spot size vs Vehicle size, time-based pricing)

### **Step 2: Identify Design Patterns**
Look for common patterns that fit the problem:
- **Strategy Pattern**: Different pricing models (BaseFare, PeakHoursFare)
- **Factory Pattern**: Creating different types of objects (ParkingSpotFactory)
- **Observer Pattern**: Notifying when spots become available
- **State Pattern**: Different states of parking spots (Available, Occupied)

### **Step 3: Plan the Architecture**
- **Separation of Concerns**: Split into logical modules
- **Single Responsibility**: Each class has one clear purpose
- **Open/Closed Principle**: Easy to extend without modifying existing code
- **Dependency Inversion**: Depend on abstractions, not concrete classes

---

## **Detailed Step-by-Step Approach**

### **Phase 1: Define Core Abstractions**

#### **1.1 Identify the Core Entities**
```python
# Core entities in parking lot system:
# - Vehicle (Car, Motorcycle, Truck)
# - ParkingSpot (Regular, Compact, Oversized, Handicapped)
# - Ticket (links Vehicle to ParkingSpot with time info)
# - FareStrategy (different pricing models)
```

#### **1.2 Create Abstract Base Classes**
```python
class Vehicle(ABC):
    """Abstract base class - defines what ALL vehicles must have"""
    
    @abstractmethod
    def get_size(self) -> VehicleSize:
        pass

class ParkingSpot(ABC):
    """Abstract base class - defines what ALL parking spots must have"""
    
    @abstractmethod
    def get_size(self) -> VehicleSize:
        pass
```

**Why Abstract Classes?**
- **Abstraction**: Hide complex implementation details
- **Polymorphism**: Treat different types uniformly
- **Extensibility**: Easy to add new vehicle/spot types

### **Phase 2: Implement Concrete Classes**

#### **2.1 Inheritance Hierarchy**
```python
class Car(Vehicle):          # Inherits from Vehicle
    def get_size(self):
        return VehicleSize.MEDIUM

class RegularSpot(ParkingSpot):  # Inherits from ParkingSpot
    def get_size(self):
        return VehicleSize.MEDIUM
```

**Benefits of Inheritance:**
- **Code Reuse**: Common behavior in base class
- **Polymorphism**: `Car` and `Truck` can be treated as `Vehicle`
- **Type Safety**: Compiler ensures all methods are implemented

#### **2.2 Polymorphism in Action**
```python
# This works because of polymorphism:
vehicles = [Car("ABC123"), Motorcycle("XYZ789"), Truck("TRK456")]
for vehicle in vehicles:
    size = vehicle.get_size()  # Each calls its own implementation
```

### **Phase 3: Design Patterns Implementation**

#### **3.1 Strategy Pattern**
```python
class FareStrategy(ABC):
    @abstractmethod
    def calculate_fare(self, ticket, base_fare):
        pass

class BaseFareStrategy(FareStrategy):
    def calculate_fare(self, ticket, base_fare):
        # Simple time-based calculation
        return base_fare * hours

class PeakHoursFareStrategy(FareStrategy):
    def calculate_fare(self, ticket, base_fare):
        # Peak hours with multiplier
        return base_fare * hours * peak_multiplier
```

**Why Strategy Pattern?**
- **Flexibility**: Can switch pricing models at runtime
- **Extensibility**: Easy to add new pricing strategies
- **Testability**: Can test each strategy independently

#### **3.2 Factory Pattern**
```python
class ParkingSpotFactory:
    @staticmethod
    def create_spot(spot_type: str, spot_number: int) -> ParkingSpot:
        if spot_type == "regular":
            return RegularSpot(spot_number)
        elif spot_type == "compact":
            return CompactSpot(spot_number)
        # ... etc
```

**Why Factory Pattern?**
- **Centralized Creation**: All object creation in one place
- **Encapsulation**: Hide complex creation logic
- **Flexibility**: Easy to change how objects are created

### **Phase 4: Business Logic Classes**

#### **4.1 Encapsulation**
```python
class Ticket:
    def __init__(self, ticket_id, vehicle, spot, entry_time):
        self.ticket_id = ticket_id
        self.vehicle = vehicle
        self.spot = spot
        self.entry_time = entry_time
        self.exit_time = None  # Private state
    
    def get_duration(self):
        # Encapsulated logic for calculating duration
        if self.exit_time is None:
            raise ValueError("Vehicle hasn't left yet")
        return self.exit_time - self.entry_time
```

**Benefits of Encapsulation:**
- **Data Protection**: Internal state is controlled
- **Validation**: Can validate data before setting
- **Maintainability**: Changes to internal logic don't affect external code

#### **4.2 Single Responsibility Principle**
```python
class ParkingManager:
    """ONLY handles parking spot management"""
    
    def park_vehicle(self, vehicle):
        # Find spot and park vehicle
        pass
    
    def unpark_vehicle(self, vehicle):
        # Remove vehicle from spot
        pass

class FareCalculator:
    """ONLY handles fare calculation"""
    
    def calculate_fare(self, ticket):
        # Calculate fare using strategy
        pass
```

**Why Single Responsibility?**
- **Maintainability**: Changes to parking logic don't affect fare calculation
- **Testability**: Can test each component independently
- **Reusability**: Components can be reused in different contexts

### **Phase 5: Composition and Orchestration**

#### **5.1 Main Parking Lot Class**
```python
class ParkingLot:
    def __init__(self, parking_manager, fare_calculator):
        self.parking_manager = parking_manager  # Composition
        self.fare_calculator = fare_calculator  # Composition
    
    def enter_vehicle(self, vehicle):
        # Orchestrates the parking process
        spot = self.parking_manager.park_vehicle(vehicle)
        if spot:
            return self.create_ticket(vehicle, spot)
        return None
```

**Benefits of Composition:**
- **Loose Coupling**: ParkingLot doesn't need to know implementation details
- **Flexibility**: Can swap different managers/calculators
- **Testability**: Can inject mock objects for testing

---

## **Key OOD Principles Demonstrated**

### **1. Encapsulation**
- **Data and behavior together**: `Ticket` class contains both data and methods
- **Information hiding**: Internal state is protected
- **Controlled access**: Methods provide safe ways to access/modify data

### **2. Inheritance**
- **Code reuse**: Common behavior in base classes
- **Type hierarchy**: `Car` is a `Vehicle`
- **Polymorphism**: Different types can be treated uniformly

### **3. Polymorphism**
- **Same interface, different behavior**: All vehicles have `get_size()` but return different values
- **Runtime binding**: The correct method is called based on actual object type
- **Extensibility**: New vehicle types work with existing code

### **4. Abstraction**
- **Hide complexity**: `ParkingLot` doesn't need to know how spots work internally
- **Focus on essentials**: Define what something should do, not how
- **Interface design**: Define clear contracts between components

### **5. Design Patterns**
- **Strategy**: Different fare calculation methods
- **Factory**: Centralized object creation
- **Composition**: Building complex objects from simpler ones

---

## **How to Apply This Approach to Any OOD Problem**

### **Step 1: Analyze the Problem**
1. **Identify nouns** (entities/objects)
2. **Identify verbs** (operations/behaviors)
3. **Identify relationships** between entities
4. **Identify constraints** and business rules

### **Step 2: Design the Class Hierarchy**
1. **Find commonalities** between similar objects
2. **Create abstract base classes** for common behavior
3. **Implement concrete classes** that inherit from base classes
4. **Use interfaces** to define contracts

### **Step 3: Apply Design Patterns**
1. **Strategy Pattern**: When you have different algorithms for the same task
2. **Factory Pattern**: When object creation is complex
3. **Observer Pattern**: When objects need to notify others of changes
4. **State Pattern**: When objects have different behaviors based on state

### **Step 4: Implement Business Logic**
1. **Encapsulate data** with related behavior
2. **Follow Single Responsibility** - each class has one reason to change
3. **Use composition** to build complex objects
4. **Keep coupling loose** between components

### **Step 5: Test and Refactor**
1. **Write tests** for each component
2. **Refactor** based on what you learn
3. **Optimize** for performance if needed
4. **Document** the design decisions

---

## **Common Mistakes to Avoid**

### **1. Over-Engineering**
- Don't add patterns just because you know them
- Start simple and add complexity only when needed
- Focus on solving the actual problem

### **2. Tight Coupling**
- Avoid direct dependencies between concrete classes
- Use interfaces and abstractions
- Depend on abstractions, not implementations

### **3. Violating Single Responsibility**
- Each class should have one clear purpose
- If a class does too many things, split it
- Methods should be focused and cohesive

### **4. Ignoring Encapsulation**
- Don't expose internal state unnecessarily
- Use getters/setters when needed
- Protect data integrity

### **5. Not Thinking About Extensibility**
- Design for future changes
- Use open/closed principle
- Make it easy to add new features

---

## **Practice Tips**

1. **Start with a simple version** and iterate
2. **Draw UML diagrams** to visualize relationships
3. **Write tests first** to understand requirements
4. **Refactor constantly** as you learn more
5. **Study existing patterns** in real-world systems
6. **Practice with different domains** (e-commerce, games, etc.)

Remember: **Good OOD is about making code that's easy to understand, maintain, and extend.** The patterns and principles are tools to achieve this goal, not ends in themselves. 