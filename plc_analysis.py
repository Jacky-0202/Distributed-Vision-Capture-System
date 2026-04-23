import serial
import asyncio
from datetime import datetime

# ==========================================
# ⚙️ Configuration (19200, 8-E-1)
# ==========================================
SERIAL_PORT = '/dev/ttyUSB0'
MY_ID = 8
PLC_ID = 1  # Responding to ID 1 to clear HMI errors
BAUDRATE = 19200
BYTESIZE = serial.EIGHTBITS
PARITY = serial.PARITY_EVEN
STOPBITS = serial.STOPBITS_ONE

# Modbus Register Pool
registers = {
    0: 0,      # 40001: Composite Command (Light + Camera Mask)
    2: 2,      # 40003: Status (1:Running, 2:OK/Ready)
    3: 0,      # 40004: Abnormal Code
    9: 1,      # 40010: Watchdog Heartbeat
    16: 100    # 40017: Firmware Version
}

# Mapping based on observed PLC sequence
LIGHT_MAP = {
    1: "RE (Infrared)",
    2: "R (Red)",
    3: "G (Green)",
    4: "B (Blue)"
}

# Tracking the last command to filter continuous writes from M1000
last_command = -1

def calculate_crc(data):
    """Calculate Modbus RTU CRC-16 checksum."""
    crc = 0xFFFF
    for pos in data:
        crc ^= pos
        for _ in range(8):
            if (crc & 1) != 0:
                crc >>= 1
                crc ^= 0xA001
            else:
                crc >>= 1
    return crc.to_bytes(2, 'little')

def handle_response(ser, slave_id, func_code, content):
    """Encapsulate and send the Modbus response packet."""
    packet = bytearray([slave_id, func_code]) + content
    packet += calculate_crc(packet)
    ser.write(packet)

def decode_command(val):
    """
    Decode composite command into Light mode and Camera Mask.
    Bits 0-3: Light ID | Bits 4-11: Camera Mask
    """
    light_id = val & 0x000F
    camera_mask = (val & 0x0FF0) >> 4
    
    light_name = LIGHT_MAP.get(light_id, f"Unknown ({light_id})")
    
    # Identify Layers based on WSUM logic
    if camera_mask == 0b11: # Dec 3
        layer = "Layer 1 (Cam 1 & 2)"
    elif camera_mask == 0b1100: # Dec 12
        layer = "Layer 2 (Cam 3 & 4)"
    else:
        layer = f"Custom Mask ({bin(camera_mask)})"
        
    return light_name, layer

async def process_photo_task(val):
    """
    Execute photo task with 2 -> 1 -> 2 handshake.
    Satisfies PLC condition 'LD= D113 K2'.
    """
    # 1. Switch to Running status
    registers[2] = 1 
    light_name, layer = decode_command(val)
    ts = datetime.now().strftime('%H:%M:%S')
    
    print(f"[{ts}] 📸 Triggered | Light: {light_name} | Target: {layer} | Status -> 1 (Running)")

    # 2. Simulate processing delay (Future: Trigger Slave CM4s via HTTP here)
    await asyncio.sleep(0.5)

    # 3. Task complete, return to OK/Ready status to release PLC step sequence
    registers[2] = 2
    print(f"[{ts}] ✅ Completed | System Ready | Status -> 2 (OK)")

async def run_master_listener():
    """Main loop for listening to ID 1 and ID 8 requests."""
    global last_command
    is_first_sync = True # Avoid triggering on script startup
    
    try:
        ser = serial.Serial(port=SERIAL_PORT, baudrate=BAUDRATE, bytesize=BYTESIZE, 
                            parity=PARITY, stopbits=STOPBITS, timeout=0.01)
        print(f"🚀 CM4 Master Listener Active (Responding to ID: {PLC_ID}, {MY_ID})")
        print(f"📊 Logic: RE->R->B->G Cycle | Startup Silent Sync: Enabled")
        print("-" * 75)

        while True:
            if ser.in_waiting >= 8:
                request = ser.read(ser.in_waiting)
                
                target_id = request[0]
                # Filter for IDs and verify CRC
                if target_id in [PLC_ID, MY_ID] and request[-2:] == calculate_crc(request[:-2]):
                    func_code = request[1]
                    addr = (request[2] << 8) | request[3]
                    
                    # --- FC03: Read Holding Registers ---
                    if func_code == 0x03:
                        qty = (request[4] << 8) | request[5]
                        data_content = bytearray([qty * 2])
                        for i in range(qty):
                            v = registers.get(addr + i, 0)
                            data_content += v.to_bytes(2, 'big')
                        handle_response(ser, target_id, 0x03, data_content)

                    # --- FC06: Write Single Register ---
                    elif func_code == 0x06:
                        val = (request[4] << 8) | request[5]
                        registers[addr] = val
                        ser.write(request) # Send ACK
                        
                        # Command Register Address 0 (40001)
                        if addr == 0 and val > 0:
                            if is_first_sync:
                                # Synchronize with PLC's current M1000 output
                                last_command = val
                                is_first_sync = False
                                print(f"[{datetime.now().strftime('%H:%M:%S')}] ⚙️ Initial Sync Complete (Value: {val})")
                            elif val != last_command:
                                # Trigger task only on actual value change
                                asyncio.create_task(process_photo_task(val))
                                last_command = val
                            
            await asyncio.sleep(0.001)
    except Exception as e:
        print(f"\n🛑 Serial Error: {e}")
    finally:
        if 'ser' in locals(): ser.close()

if __name__ == "__main__":
    asyncio.run(run_master_listener())