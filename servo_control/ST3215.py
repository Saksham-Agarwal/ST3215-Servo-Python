import sys
sys.path.append("..")


from scservo_sdk import *                   # Uses SC Servo SDK library

class ST3215:
    def __init__(self, device_name, baudrate=1000000, speed=2400, acceleration=50):
        self.portHandler = PortHandler(device_name)
        self.packetHandler = sms_sts(self.portHandler)
        self.SCS_MOVING_SPEED = speed
        self.SCS_MOVING_ACC = acceleration
        

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

        if result != COMM_SUCCESS:
            print(f" Not working, [ID:{servo_id:03d}] Comm Error: {self.packetHandler.getTxRxResult(result)}")
            return False

        if error != 0:
            print(f" Not working, [ID:{servo_id:03d}] Hardware Error: {self.packetHandler.getRxPacketError(error)}")
            return False

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
    
    def change_id(self, current_id, new_id):
        """
        Unlocks EPROM, changes the servo ID, and locks EPROM.
        WARNING: It is highly recommended to only have ONE servo physically 
        connected to the board when performing this action to prevent accidents.
        """
        # IDs must be between 0 and 253 (254 is the broadcast ID)
        if not (0 <= new_id <= 253):
            print("Error: New ID must be between 0 and 253.")
        print(f"Attempting to change servo ID from {current_id} to {new_id}...")

        # Step 1: Unlock EPROM
        result, error = self.packetHandler.unLockEprom(current_id)
        if result != COMM_SUCCESS or error != 0:
            print("Failed to unlock EPROM.")
            return False

        # Step 2: Write the new ID to the ID register ('scs_id' is defined in the SDK)
        result, error = self.packetHandler.write1ByteTxRx(current_id, scs_id, new_id)
        if result != COMM_SUCCESS:
            print(f"Write Comm Error: {self.packetHandler.getTxRxResult(result)}")
            return False
        if error != 0:
            print(f"Write Hardware Error: {self.packetHandler.getRxPacketError(error)}")
            return False

        self.packetHandler.LockEprom(current_id) 
        
        print(f"Successfully changed Servo ID from {current_id} to {new_id}!")
        return True

    def write_angle(self, servo_id, angle):
        scs_comm_result, scs_error = self.packetHandler.WritePosEx(servo_id, angle, self.SCS_MOVING_SPEED, self.SCS_MOVING_ACC)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(scs_error))

    def read_angle_speed(self, servo_id):
        scs_present_position, scs_present_speed, scs_comm_result, scs_error = self.packetHandler.ReadPosSpeed(servo_id)
        if scs_comm_result != COMM_SUCCESS:
            print(self.packetHandler.getTxRxResult(scs_comm_result))
        # else:
        #     print("[ID:%03d] PresPos:%d PresSpd:%d" % (servo_id, scs_present_position, scs_present_speed))
        if scs_error != 0:
            print(self.packetHandler.getRxPacketError(scs_error))
        
        return scs_present_position, scs_present_speed
    
    def wheel(self, servo_id, rot_speed):
        scs_comm_result, scs_error = self.packetHandler.WheelMode(servo_id)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(scs_comm_result))
        elif scs_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(scs_error))   
        
        scs_comm_result, scs_error = self.packetHandler.WriteSpec(servo_id, rot_speed, self.SCS_MOVING_ACC)
        if scs_comm_result != COMM_SUCCESS:
            print("%s" % self.packetHandler.getTxRxResult(scs_comm_result))
        if scs_error != 0:
            print("%s" % self.packetHandler.getRxPacketError(scs_error))

    def ReadCurrent(self, servo_id):
        scs_current_current, scs_comm_result, scs_error = self.packetHandler.ReadCurrent(servo_id)
        if scs_comm_result != COMM_SUCCESS:
            print(self.packetHandler.getTxRxResult(scs_comm_result))
        # else:
        #     print("[ID:%03d] Current Current:%d" % (servo_id, scs_current_current))
        if scs_error != 0:
            print(self.packetHandler.getRxPacketError(scs_error))
        return scs_current_current

    def ReadTemp(self, servo_id):
        scs_current_temperature, scs_comm_result, scs_error = self.packetHandler.ReadTemp(servo_id)
        if scs_comm_result != COMM_SUCCESS:
            print(self.packetHandler.getTxRxResult(scs_comm_result))
            
        # else:
        #     print("[ID:%03d] Current Temperature:%d" % (servo_id, scs_current_temperature))
        if scs_error != 0:
            print(self.packetHandler.getRxPacketError(scs_error))
        scs_current_temperature = scs_current_temperature * 6.5
        return scs_current_temperature
    
    def close(self):
        self.portHandler.closePort()
        print("Port closed.")
        

