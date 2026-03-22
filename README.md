# ST3215 Servo Python Library

This project provides a simple Python interface for controlling the **ST3215 bus servo** using the Waveshare Bus Servo Adapter.

It builds upon the original Waveshare examples and restructures them into a cleaner, easier-to-use format—similar to how standard hobby servos are used.

---

## Features

* Easy-to-use Python API for ST3215 servos
* Based on Waveshare communication protocol
* Simplified commands for position, speed, and control
* Designed for quick integration into robotics projects

---

## Background

The original Waveshare resources for ST3215 servos were difficult to locate and not well structured. This repository consolidates the required code and improves usability for developers.

---

## Requirements

* Python 3.x
* Waveshare Bus Servo Adapter
* ST3215 Servo
* `pyserial==3.5`

---

## Installation

```bash
git clone https://github.com/Saksham-Agarwal/ST3215-Servo-Python.git
cd ST3215-Servo-Python
```

---

## Setup (Virtual Environment) [for windows]

```bash
python -m venv .venv
.venv\Scripts\activate

# Install dependencies
pip install -r requirements.txt

# Deactivate environment
deactivate
```


## Setup (Virtual Environment) [for ubuntu]

```bash
python3 -m venv .venv
source .venv/bin/activate
# Install dependencies
pip install -r requirements.txt

# Deactivate environment
deactivate
```
---

## Example

```python
from servo_control.ST3215 import ST3215

bus = ST3215("COM5")

ids = bus.scan()
print(ids)

bus.write_angle(ids[0], 2048)

bus.close()
```

---

## API Reference

### `ST3215(device_name, baudrate=1000000, speed=2400, acceleration=50)`

Initializes the servo bus connection.

* **device_name**: Serial port (e.g., `COM5`, `/dev/ttyUSB0`)
* **baudrate**: Communication speed (default: 1 Mbps)
* **speed**: Default movement speed
* **acceleration**: Default acceleration

---

### `check_servo(servo_id)`

Checks if a servo is connected and responding.

* **servo_id**: ID of the servo
* **Returns**: `True` if detected, else `False`

---

### `scan(start=0, end=20)`

Scans a range of IDs and finds connected servos.

* **start**: Starting ID
* **end**: Ending ID
* **Returns**: List of detected servo IDs

---

### `change_id(current_id, new_id)`

Changes the ID of a servo.

* **current_id**: Existing ID
* **new_id**: New ID (0–253)

⚠️ **Important:** Only one servo should be connected while performing this operation.

* **Returns**: `True` if successful

---

### `write_angle(servo_id, angle)`

Moves the servo to a specific position.

* **servo_id**: Servo ID
* **angle**: Target position (raw value, typically `0–4095`)

---

### `read_angle_speed(servo_id)`

Reads current position and speed of a servo.

* **servo_id**: Servo ID
* Prints position and speed

---

### `wheel(servo_id, rot_speed)`

Sets the servo to continuous rotation mode.

* **servo_id**: Servo ID
* **rot_speed**: Rotation speed (sign = direction, magnitude = speed)

---

### `close()`

Closes the serial port connection.
