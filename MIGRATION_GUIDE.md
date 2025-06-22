# Migration Guide: Manual Build → Modern Gradle

Complete guide for migrating Object-Oriented Design projects from manual builds to modern Gradle with VS Code integration.

## Key Improvements

✅ **In-place migration** - No separate directories  
✅ **Preserve original structure** - Keep existing files as reference  
✅ **Simple directory mapping** - Direct project directory mapping  
✅ **Clean multi-project setup** - All projects in one workspace  

## Migration Process

### Step 1: Set Up Multi-Project Structure

Create root-level Gradle files:

**settings.gradle**
```gradle
rootProject.name = 'oo-design'

include 'vendingmachine'
include 'atm'
// ... other projects

// Map to actual directories
project(':vendingmachine').projectDir = file('Vending_Machine_Code')
project(':atm').projectDir = file('ATM_Code')
// ... other mappings
```

**build.gradle** (root)
```gradle
subprojects {
    apply plugin: 'java'
    
    repositories {
        mavenCentral()
    }
    
    dependencies {
        testImplementation 'org.junit.jupiter:junit-jupiter:5.11.0'
        testRuntimeOnly 'org.junit.platform:junit-platform-launcher'
    }
    
    java {
        toolchain { languageVersion = JavaLanguageVersion.of(17) }
        sourceCompatibility = JavaVersion.VERSION_17
        targetCompatibility = JavaVersion.VERSION_17
    }
    
    tasks.named('test') { useJUnitPlatform() }
}
```

### Step 2: Migrate Individual Project

For each project directory (e.g., `Vending_Machine_Code/`):

1. **Update the original README**:
   ```bash
   cd Vending_Machine_Code/vendingmachine
   # Update existing README.md to include:
   # - Gradle build instructions
   # - All valuable original content (features, classes, test coverage)
   # - Remove references to manual builds (readers have no context)
   
   # All source files stay exactly as-is
   ```

2. **Create project build.gradle with custom source paths**:
   ```gradle
   plugins {
       id 'java'
   }
   
   // Configure source directories to use original paths
   sourceSets {
       main {
           java {
               srcDir 'vendingmachine'
               exclude '**/*Test.java'  // Exclude test files from main
           }
       }
       test {
           java {
               srcDir 'vendingmachine'
               include '**/*Test.java'  // Include only test files
           }
       }
   }
   ```


### Step 3: Test Migration

```bash
# From root directory
./gradlew :vendingmachine:build
./gradlew :vendingmachine:test
```

### Step 4: Verify Multi-Project Setup

```bash
./gradlew projects  # Should show all projects
./gradlew buildAll  # Build everything
```

## Directory Structure After Migration

```
oo-design/
├── build.gradle                    # Root build configuration
├── settings.gradle                 # Multi-project setup
├── gradlew, gradlew.bat           # Gradle wrapper
├── gradle/                        # Wrapper files
├── .vscode/                       # VS Code configuration
│
├── Vending_Machine_Code/          # Original directory (migrated)
│   ├── build.gradle              # Project-specific config (only new file!)
│   └── vendingmachine/           # Original directory completely unchanged
│       ├── README.md             # Updated with Gradle instructions
│       ├── *.java                # All source and test files
│       └── combined.plantuml     # UML diagrams in original location
│
├── ATM_Code/                     # Next project to migrate
├── Blackjack_Code/              # Next project to migrate
└── ...
```

## Benefits of In-Place Migration

### Before
```bash
# Each project had separate build process
cd Vending_Machine_Code/vendingmachine
mkdir lib
curl -L <url> -o lib/junit.jar
javac -cp lib/junit.jar *.java
java -jar lib/junit-platform.jar --scan-classpath
```

### After  
```bash
# From root directory
./gradlew :vendingmachine:test
./gradlew :atm:test
./gradlew :blackjack:test
```

## VS Code Integration

Opening the root folder provides:
- **All projects in one workspace**
- **Gradle tasks for each project**
- **Unified debugging and testing**
- **No context switching between projects**

## Migration Checklist

For each project:

- [ ] Create project `build.gradle` with custom source paths
- [ ] Update original README with Gradle instructions  
- [ ] Test: `./gradlew :project:build test`
- [ ] Update root README with project status
- [ ] Configure test output visibility (optional but recommended):
  ```gradle
  tasks.named('test') {
      useJUnitPlatform()
      testLogging {
          showStandardStreams = true
      }
      outputs.upToDateWhen { false }  // Always run tests, never cache
  }
  ```

## Key Advantages

1. **Preserves History**: Original files remain intact
2. **No Confusion**: Single source of truth per project  
3. **Easy Navigation**: All projects accessible from root
4. **Professional Structure**: Industry-standard Gradle layout
5. **IDE Friendly**: Full VS Code integration
6. **Reader Friendly**: One command to run any project

This approach transforms the repository into a professional, cohesive development environment while preserving the original educational structure.