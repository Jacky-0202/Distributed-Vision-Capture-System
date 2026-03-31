---
tags:
---
## 程式碼

```python
import serial
import time
```

```python
# =============================================================================
# 1. Configuration Layer
# =============================================================================
class ModbusConfig:
    """Centralized configuration for Serial and Modbus parameters."""
    PORT = '/dev/ttyUSB0'          # Linux device path for RS485 adapter
    BAUDRATE = 19200               # Transmission speed
    PARITY = serial.PARITY_EVEN    # Even parity (Industrial standard)
    SLAVE_ID = 8                   # Unique Station ID for this CM4
    
    # Internal Memory Map (Modbus Holding Registers)
    REGISTERS = {
        0: 0,    # 40001: Combined Command (Buttons + Lights)
        2: 1,    # 40003: System Status (1 = Running)
        3: 0,    # 40004: Abnormal/Alarm (0 = Normal)
        16: 100  # 40017: Software Version (100 = v1.00)
    }
    
    # List of addresses to ignore in console logs to prevent spamming
    SILENT_ADDR = [2, 3, 16]
```

```python
# =============================================================================
# 2. Utility Layer
# =============================================================================
def calculate_crc(data):
    """
    Calculates the Modbus RTU 16-bit CRC (Cyclic Redundancy Check).
    Ensures data integrity over the RS485 line.
    """
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001  # Modbus Polynomial
            else:
                crc >>= 1
    return crc.to_bytes(2, 'little')
```

```python
# =============================================================================
# 3. Decoder Layer (Logic Translation)
# =============================================================================
class CommandDecoder:
    """Translates raw Modbus register data into human-readable labels."""
    
    # Mapping for the Light Index (Bits 0-3)
    LIGHT_MAP = {1: "R", 2: "RE", 3: "B", 4: "G"}

    @staticmethod
    def decode_addr_0(val):
        """
        Deconstructs the 16-bit value of Register 0.
        Format: [Reserved 4-bits][Buttons 8-bits][Lights 4-bits]
        """
        # 1. Extract Light Index (The last 4 bits)
        light_idx = val & 0x000F
        light_name = CommandDecoder.LIGHT_MAP.get(light_idx, "OFF")
        
        # 2. Extract 8 Functional Buttons (Bits 4 to 11)
        # Shift right by 4 bits to align Button 1 to the first bit
        btn_area = (val & 0x0FF0) >> 4
        active_buttons = [f"#{i+1}" for i in range(8) if (btn_area >> i) & 1]
        
        return light_name, active_buttons if active_buttons else ["None"]
```

```python
# =============================================================================
# 4. Communication Layer (Modbus Slave Engine)
# =============================================================================
class ModbusSlave:
    def __init__(self, config):
        self.cfg = config
        self.ser = serial.Serial(
            port=self.cfg.PORT,
            baudrate=self.cfg.BAUDRATE,
            parity=self.cfg.PARITY,
            timeout=0.05
        )

    def handle_read(self, addr):
        """Handles Modbus Function Code 03: Read Holding Registers."""
        val = self.cfg.REGISTERS.get(addr, 0)
        # Build Response: [ID][FC][ByteCount][Data_H][Data_L]
        response = bytearray([self.cfg.SLAVE_ID, 0x03, 0x02])
        response.extend(val.to_bytes(2, 'big'))
        self.ser.write(response + calculate_crc(response))

    def handle_write(self, addr, val, raw_request):
        """Handles Modbus Function Code 06: Write Single Register."""
        # Update internal memory
        self.cfg.REGISTERS[addr] = val
        
        # Send Acknowledgement (ACK): Echo the exact request packet
        self.ser.write(raw_request)
        
        # Log decoding results for Register 0
        if addr == 0:
            light, btns = CommandDecoder.decode_addr_0(val)
            self.log_action(light, btns, val)

    def run(self):
        """Main loop to listen and respond to PLC requests."""
        print(f"🚀 Modbus Slave Active [ID: {self.cfg.SLAVE_ID}]")
        print(f"📡 Serial Config: {self.cfg.BAUDRATE}, {self.cfg.PARITY}")
        
        try:
            while True:
                if self.ser.in_waiting >= 8:
                    req = self.ser.read(self.ser.in_waiting)
                    
                    # Security Check: Verify Slave ID and CRC Checksum
                    if req[0] == self.cfg.SLAVE_ID and req[-2:] == calculate_crc(req[:-2]):
                        func = req[1]
                        addr = (req[2] << 8) | req[3]
                        
                        if func == 3:   # Read Request
                            self.handle_read(addr)
                        
                        elif func == 6: # Write Request
                            value = (req[4] << 8) | req[5]
                            self.handle_write(addr, value, req)
                                
                time.sleep(0.005) # 5ms polling to prevent CPU spikes
        except KeyboardInterrupt:
            print("\n🛑 Server stopped by user.")
        finally:
            self.ser.close()

    def log_action(self, light, btns, raw_val):
        """Prints decoded information to the console."""
        timestamp = time.strftime('%H:%M:%S')
        print(f"[{timestamp}] 📥 COMMAND RECEIVED")
        print(f"   💡 Lighting Mode : [ {light:3} ]")
        print(f"   🔘 Active Buttons: [ {', '.join(btns)} ]")
        print(f"   📦 Raw Data Value: {raw_val} (0x{raw_val:04X})")
        print("-" * 50)
```

```python
# =============================================================================
# Execution Entry Point
# =============================================================================
if __name__ == "__main__":
    # Initialize and start the slave using the provided configuration
    slave = ModbusSlave(ModbusConfig)
    slave.run()
```
