# AI-Avengers
Optimizing Traffic Control: Dynamic Green Light Allocation and Emergency Vehicle Prioritization for Four-Lane Systems

### Table of Contents
1. [Introduction]
2. [Features]
3. [Technology Stack]
4. [Usage]
5. [Contributing]

## Introduction

**Optimizing Traffic Control** is an advanced system designed to manage traffic at four-lane intersections dynamically. It allocates green light durations based on real-time vehicle counts captured from cameras placed at each lane. The system also prioritizes emergency vehicles such as ambulances and fire engines by altering traffic signals to clear a path when they are within a defined proximity of the intersection.

### Key Objectives:
- Improve traffic flow and reduce congestion through dynamic signal adjustments.
- Enable real-time detection and prioritization of emergency vehicles to minimize delays.
- Use machine learning models to adapt and optimize traffic control patterns.

## Features

- **Dynamic Green Light Allocation**: Uses vehicle counts from three cameras in each lane to dynamically adjust the green light timing based on traffic volume.
- **Emergency Vehicle Prioritization**: Detects emergency vehicles within a 3km radius and gives them priority by turning the respective lane's signal green when the vehicle is 750m away.
- **Real-Time Vehicle Detection**: Uses camera feeds and machine learning to detect and count vehicles during red light intervals.
- **AI-Based Optimization**: Employs machine learning to optimize traffic light durations based on historical traffic data and real-time inputs.

## Technology Stack

- **Programming Language**: Python
- **Libraries and Frameworks**:
  - **Kivy**: For building the app.
  - **Figma**: User interface (UI/UX) of the system.
  - **OpenCV**: Used for real-time vehicle detection and counting from traffic camera feeds.
  - **Google Maps API** (Optional): Used for tracking the real-time location of emergency vehicles.
  - **Requests**: For handling HTTP requests between the client and server.
  - **Intel oneAPI**: For hardware acceleration and optimized AI model inference.
  
- **Hardware**: Cameras for traffic detection, a local server for handling communication, and devices for location tracking.
- **Tools**: 
  - **GitHub**: For version control and collaboration.
  - **Intel DevCloud**: For deploying AI models with hardware acceleration using Intel oneAPI.

## Installation

### Prerequisites
- Python 3.x installed on your system.
- Camera feeds for each lane at the traffic signal.


Usage
Dynamic Green Light Allocation
The system dynamically adjusts the green light duration based on vehicle counts from each lane. Traffic cameras positioned 500m apart along the lane capture the vehicle flow.
The lane with the highest vehicle count receives an extended green light duration, and the timings are recalculated at regular intervals.
Emergency Vehicle Prioritization
When an emergency vehicle (like an ambulance or fire engine) is detected within 1 km of the intersection, the system will alert nearby traffic signals.
If the emergency vehicle is within 250m of the intersection, the corresponding lane's signal turns green, clearing the path.

Real-time data from cameras will automatically adjust traffic lights based on vehicle counts.
Simulating Emergency Vehicles:
Simulate an emergency vehicle by sending location data to the server. The system will prioritize the lane where the vehicle is detected.

## Emergency Vehicle App

The **Emergency Vehicle App** is a crucial component of the system, designed to facilitate real-time communication between emergency vehicles and traffic signals.

### Features:
- **Real-time GPS Tracking**: Tracks the location of emergency vehicles (e.g., ambulances, fire engines) using GPS.
- **Emergency Signal Transmission**: Sends an alert to nearby traffic signals when an emergency vehicle is within 3km of the junction.
- **Proximity Alerts**: When the vehicle is 750m away from the traffic signal, the app ensures that the respective lane receives a green signal to prioritize the vehicle's movement.
- **User Interface**:
  - The app has two profiles: one for the emergency vehicle and one for the traffic junction operator.
  - **Emergency Vehicle Profile**: Contains an "Emergency Alert" button that sends real-time notifications to nearby traffic lights.
  - **Junction Profile**: Displays vehicle information (vehicle type, license plate number, ETA) and allows operators to monitor traffic conditions.

### App Workflow:
1. **Login**: Users can select between the emergency vehicle profile or the junction profile upon login.
2. **Emergency Vehicle Operation**: After login, the emergency vehicle operator can press an alert button to notify traffic signals.
3. **Junction Monitoring**: Junction operators can see incoming emergency vehicles and make manual adjustments if necessary.
4. **Profile Information**: Both profiles (vehicle and junction) contain editable information fields for operators to input relevant details.

## Installation

To get started with the project, follow these steps:

1. Clone the repository:
    ```bash
    git clone https://github.com/username/repository.git
    ```
2. Install dependencies:
    ```bash
    cd repository
    pip install -r requirements.txt
    ```

3. Run the project:
    ```bash
    python main.py
    ```

## Usage

To use the project, you can follow the examples below:

1. Run the project:
    ```bash
    python main.py
    ```
2. Example usage of a specific feature:
    ```bash
    python main.py --feature
    ```

##Figma Link of the Prototype:
  https://www.figma.com/proto/yIPBGPUdlKjEDgRDTSbQXL/Emergency-Vehicle-App?node-id=44-63&t=9gr0e8wTj5Bxisdg-1
  
##Figma Link of the Design:
    https://www.figma.com/design/yIPBGPUdlKjEDgRDTSbQXL/Emergency-Vehicle-App?node-id=0-1&node-type=canvas&t=2rBoMFqcDyklzSkp-0
    
