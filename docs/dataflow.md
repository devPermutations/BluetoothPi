# Bluetooth Device Scanner Data Flow

## System Data Flow Overview

```mermaid
graph TD
    A[Bluetooth Scanner Service] -->|Device Discovery| B[Device Classifier]
    B -->|Classified Data| C[Data Storage]
    D[Configuration] -->|Settings| A
    D -->|Rules| B
    E[Logging System] -->|Logs| A
    E -->|Logs| B
    E -->|Logs| C
```

## Component Interaction Flow

```mermaid
sequenceDiagram
    participant Scanner as Bluetooth Scanner
    participant BlueZ as BlueZ D-Bus
    participant Classifier as Device Classifier
    participant Storage as Data Storage
    participant Config as Configuration
    participant Logger as Logging System

    Scanner->>Config: Load Configuration
    Scanner->>BlueZ: Initialize Connection
    Scanner->>BlueZ: Start Scanning
    BlueZ-->>Scanner: Device Discovered
    Scanner->>Classifier: Process Device
    Classifier->>Config: Get Classification Rules
    Classifier-->>Scanner: Classification Result
    Scanner->>Storage: Store Device Data
    Scanner->>Logger: Log Discovery
    Classifier->>Logger: Log Classification
    Storage->>Logger: Log Storage Operation
```

## Data Processing Flow

```mermaid
graph LR
    A[Raw Device Data] -->|Parse| B[Device Properties]
    B -->|Analyze| C[Device Classification]
    C -->|Store| D[Device Database]
    D -->|Query| E[Analytics]
    D -->|Cleanup| F[Data Retention]
```

## Device Classification Flow

```mermaid
graph TD
    A[Device Discovery] -->|Extract Properties| B[Device Properties]
    B -->|Check Class| C{Is Mobile?}
    C -->|Yes| D[Mobile Phone]
    C -->|No| E[Other Device]
    D -->|Store| F[Device Database]
    E -->|Store| F
    F -->|Generate| G[Device Statistics]
```

## Data Storage Schema

```mermaid
erDiagram
    DEVICE ||--o{ SCAN_RESULT : has
    DEVICE {
        string mac_address
        string device_name
        string device_class
        string manufacturer
        datetime first_seen
        datetime last_seen
    }
    SCAN_RESULT ||--o{ DEVICE_PROPERTY : contains
    SCAN_RESULT {
        datetime scan_time
        int signal_strength
        string device_type
        boolean is_mobile
    }
    DEVICE_PROPERTY {
        string property_name
        string property_value
        datetime timestamp
    }
```

## Notes

### Data Flow Considerations
1. **Real-time Processing**
   - Device discovery events are processed immediately
   - Classification happens in real-time
   - Storage operations are asynchronous

2. **Data Integrity**
   - All device data is validated before storage
   - Duplicate entries are handled appropriately
   - Data consistency is maintained across components

3. **Performance Optimization**
   - Batch processing for storage operations
   - Caching of frequently accessed data
   - Efficient query patterns for analytics

4. **Error Handling**
   - Graceful degradation on component failure
   - Data recovery mechanisms
   - Comprehensive error logging 