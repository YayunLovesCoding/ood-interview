# Object-Oriented Design Examples

Companion code repository for "Object-Oriented Design Interview" by ByteByteGo.

## Quick Start

```bash
git clone <repo-url>
cd oo-design

# Build all projects
./gradlew buildAll

# Test a specific project
./gradlew :vendingmachine:test
./gradlew :blackjack:test
./gradlew :tictactoe:test
```

## Available Projects

| Project | Command |
|---------|---------|
| ATM System | `./gradlew :atm:test` |
| Blackjack | `./gradlew :blackjack:test` |
| Elevator System | `./gradlew :elevator:test` |
| File Search | `./gradlew :filesearch:test` |
| Grocery Store | `./gradlew :grocerystore:test` |
| Movie Ticket | `./gradlew :movieticket:test` |
| Parking Lot | `./gradlew :parkinglot:test` |
| Restaurant | `./gradlew :restaurant:test` |
| Shipping Locker | `./gradlew :shippinglocker:test` |
| Tic-Tac-Toe | `./gradlew :tictactoe:test` |
| Vending Machine | `./gradlew :vendingmachine:test` |

## Requirements

- **Java 17+** (Java 21 LTS recommended)

## Project Commands

```bash
# List all available projects
./gradlew projects

# Build specific project
./gradlew :vendingmachine:build

# Test specific project
./gradlew :vendingmachine:test

# Build everything
./gradlew buildAll

# Test everything
./gradlew runAllTests
```

## Running Tests

Tests are configured to always show output (stdout/stderr) and run every time (no caching). This makes it easier to see test results and debug issues.

```bash
# Run tests for a specific project
./gradlew :vendingmachine:test

# If you need to force re-run cached tests in other projects
./gradlew :projectname:cleanTest :projectname:test
```
