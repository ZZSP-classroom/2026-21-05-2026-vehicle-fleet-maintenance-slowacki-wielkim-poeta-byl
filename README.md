[![Open in Visual Studio Code](https://classroom.github.com/assets/open-in-vscode-2e0aaae1b6195c2367325f4f02e2d04e9abb55f0b24a779b69b11b9e10269abc.svg)](https://classroom.github.com/online_ide?assignment_repo_id=24025472&assignment_repo_type=AssignmentRepo)
# VehicleFleetMaintenance

This repository contains the backend system for a comprehensive motor fleet management
platform built with Python and FastAPI. The system tracks vehicle specifications (ranging
from daily drivers to performance models like the Porsche 911 or classic cars like the FSO
Polonez), manages maintenance schedules, handles parts inventory, and processes vehicle
telemetry data. The project is structured to enforce Object-Oriented Programming (OOP)
principles, modern API design, and robust DevOps practices.

Exemplary structure:
```
├── app/
│ ├── main.py
│ ├── api/
│ │ ├── dependencies.py
│ │ └── endpoints/
│ ├── core/
│ │ └── config.py
│ ├── models/
│ ├── schemas/
│ ├── crud/
│ └── db/
```

Project structure:
<img width="1048" height="601" alt="image" src="https://github.com/user-attachments/assets/a3196633-922c-4f9c-a9f9-1b78a01a9632" />



Functional requirements:
1. Vehicle Registry & Management
  - CRUD Operations: Add, update, view, and remove vehicles from the fleet.
  - Technical Specifications: Store detailed attributes for each vehicle, including VIN, make, model, year, engine type, and specialized mechanical configurations.
  - Status Tracking: Monitor whether a vehicle is active, in the shop, or decommissioned.

2. Maintenance & Service Logging
 - Service History: Log all repairs, oil changes, part replacements, and inspections.
 - Scheduled Reminders: Implement background tasks to flag vehicles that are due for upcoming routine maintenance based on mileage or time intervals.

3. Parts & Inventory Tracking
 - Warehouse Management: Keep track of available spare parts, including quantities, part numbers, and suppliers.
 - Vehicle Compatibility: Link specific parts in the inventory to the vehicle models they are compatible with.

4. Telemetry Data Ingestion
  - Real-Time Data Processing: Provide high-throughput endpoints to receive simulated telemetry data from active vehicles (e.g., current speed, engine RPM, coolant temperature).
  - Data Validation: Ensure all incoming sensor data is strictly validated before being committed to the database.

5. Analytics & Reporting
  - Data Export: Generate downloadable reports summarizing fleet health, maintenance costs, and common telemetry anomalies.
  - Data Processing: Utilize data analysis libraries to aggregate and format large sets of service records into easily digestible formats (like CSV or Excel).
