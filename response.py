from serial.tools.list_ports import comports
import serial
from struct import pack, unpack
from utils import crc8, PACKET_HEADER, PACKET_FOOTER

def get_json_from_packet(packet:bytes):
    
    # Check packet header
    if packet[:2] != PACKET_HEADER:                     
        raise Warning("INVALID PACKET HEADER")
    print(f'packet header: {packet[:2]}')        

    json_supposed_len, = unpack('<I', packet[2:6]) 
    print(f'packet length: {packet[2:6]}')
        
    # Extract JSON message
    json_bytes = packet[6:-3]
    json_str = json_bytes.decode()                           
    print(f'packet json: {json_str}')
    
    # Extract alleged length of JSON message 
    # (interpret bytes as an unsigned integer)
    if (json_supposed_len != len(json_bytes)):
        raise Warning("MESSAGE LENGTH MISMATCH")
    
    # Extract CRC
    crc = packet[-3] 
    crc_packet = packet[-3:-2]                                  
    print(f'packet crc: {crc_packet}')
    if (crc != crc8(json_bytes)):
        raise Warning("CRC MISMATCH")
    
    # Check packet footer
    packet_footer = packet[-2:]
    if packet_footer != PACKET_FOOTER:                    
        raise Warning("INVALID PACKET FOOTER")    
    print(f'packet footer: {packet_footer}')
            
    return json_str

def main():    

    port_name = '/dev/ttys016'    
    # port_name = '/dev/tty.usbserial-54790373251'
    s = serial.Serial(
        port_name, 
        baudrate=115200,
        bytesize = serial.EIGHTBITS,
        stopbits = serial.STOPBITS_ONE, 
        parity = serial.PARITY_NONE,
        timeout=None
    )
    while True:     
        if s.in_waiting > 0:               
            resp_packet = s.read_until(PACKET_FOOTER) 
            print('- - - Response from API - - -')           
            print(f'packet (raw): {resp_packet}')
            resp_json = get_json_from_packet(resp_packet)                      

if __name__ == '__main__':
    main()
