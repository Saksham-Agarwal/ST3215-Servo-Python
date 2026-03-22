import sys
sys.path.append("..")


from scservo_sdk import *                   # Uses SC Servo SDK library

class ST3215:
    def __init__(self, device_name, baudrate=1000000):
        self.portHandler = PortHandler(device_name)
        self.packetHandler = sms_sts(self.portHandler)

        # Fail fast if hardware isn't responding
        if not self.portHandler.openPort():
            raise Exception(f"Failed to open port: {device_name}")

        if not self.portHandler.setBaudRate(baudrate):
            raise Exception(f"Failed to set baudrate: {baudrate}")

        print(f"Port {device_name} opened successfully at {baudrate} bps.")

    def check_servo(self, servo_id):
        """
        Pings a single servo ID and prints detailed success or error messages.
        Returns True if the servo is present and healthy, False otherwise.
        """
        print(f"Checking Servo ID {servo_id}...")
        model, result, error = self.packetHandler.ping(servo_id)

        # 1. Check for communication timeouts or wire issues
        if result != COMM_SUCCESS:
            print(f" Not working, [ID:{servo_id:03d}] Comm Error: {self.packetHandler.getTxRxResult(result)}")
            return False

        # 2. Check for internal hardware errors on the servo itself (e.g., overheating, overload)
        if error != 0:
            print(f" Not working, [ID:{servo_id:03d}] Hardware Error: {self.packetHandler.getRxPacketError(error)}")
            return False

        # 3. Success
        print(f" [ID:{servo_id:03d}] Succeeded! SC Servo model number: {model}")
        return True

    def scan(self, start=0, end=20):
        """Scans a range of IDs quietly and returns a list of active ones."""
        found = []
        print(f"Scanning IDs from {start} to {end}...")
        for i in range(start, end + 1):
            model, result, error = self.packetHandler.ping(i)
            if result == COMM_SUCCESS and error == 0:
                print(f"Found servo at ID: {i:03d} | Model: {model}")
                found.append(i)
        
        print(f"Scan complete. Found {len(found)} servos.")
        return found

    def close(self):
        self.portHandler.closePort()
        print("Port closed.")
        


# Initialize the bus (replace 'COM3' or '/dev/ttyUSB0' with your actual port)
my_bus = ST3215('COM5')



# Clean up
my_bus.close()