from serial.tools.list_ports import comports
from serial import Serial
from struct import pack, unpack
import argparse
from utils_mac import crc8, PACKET_HEADER, PACKET_FOOTER
from typing import Final, NoReturn
from time       import time, sleep

PORT_DESCRIPTION = 'Gadget Serial'
PORT_NAME = None

def contsruct_payload_from_json(json_str:str):

    json_bytes = json_str.encode()                      # Convert string to bytes
    crc = crc8(json_bytes)

    print('- - - - Request from app - - - - -') 
    print(f'packet header: {PACKET_HEADER}')    
    print(f'packet length: {pack("<I", len(json_str))}')
    print(f'packet json: {json_bytes}')
    print(f'packet crc: {crc.to_bytes(1, "little", signed=False)}, crc={crc}')
    print(f'packet crc.to_bytes, {crc.to_bytes(1, "little")}')
    print(f'packet footer: {PACKET_FOOTER}')    

    return b''.join([
        PACKET_HEADER,
        pack("<I", len(json_str)),                      # Convert length to unsigned integer byte representation        
        json_bytes,
        crc.to_bytes(1, 'little', signed=False),        # Convert CRC to byte representation
        PACKET_FOOTER
    ])

def main() -> NoReturn:
    global PORT_NAME
    parser=argparse.ArgumentParser()
    parser.add_argument("--command", help="Must be a valid command, like: get_device_info, start_cm, cancel_cm, etc.")  
    args=parser.parse_args()    
    cmd = args.command
    print(f'Sending command: {cmd}')

    while PORT_NAME is None:
        ports = comports()
        for port, desc, hwid in ports:            
            if PORT_DESCRIPTION in desc:
                PORT_NAME = port                
                break                                        
        sleep(0.5)
        print('Waiting for port information...')

    s = Serial(PORT_NAME, baudrate=115200)    
    msg = contsruct_payload_from_json(cmd)
    print(f'\nsending: {msg}')        
    s.write(msg)    

if __name__ == '__main__':
    main()
