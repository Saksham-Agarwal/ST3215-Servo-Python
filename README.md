# ST3215 Servo Python Library

This project provides a simple Python interface for controlling the ST3215 bus servo using the Waveshare Bus Servo Adapter.

It builds upon the original Waveshare examples and restructures them into a cleaner, easier-to-use format—similar to how standard hobby servos are used.

## Features
- Easy-to-use Python API for ST3215 servos
- Based on Waveshare communication protocol
- Simplified commands for position, speed, and control
- Designed for quick integration into robotics projects

## Background
The original Waveshare resources for ST3215 servos were difficult to locate and not well structured. This repository consolidates the required code and improves usability for developers.

## Requirements
- Python 3.x
- Waveshare Bus Servo Adapter
- ST3215 Servo
- pyserial==3.5

## Installation
```bash
git https://github.com/Saksham-Agarwal/ST3215-Servo-Python.git
cd ST3215-Servo-Python
pip install -r requirements.txt