from serial import Serial
import argparse
from utils import contsruct_payload_from_json

def main():
    port_name = '/dev/cu.usbmodem2101'
    # port_name = 'COM11'  
     
    parser=argparse.ArgumentParser()
    parser.add_argument("--command", help="Must be a valid command, like: get_device_info, start_cm, cancel_cm, etc.")  
    args=parser.parse_args()    
    cmd = args.command
    print(f'Sending command: {cmd}')

    s = Serial(port_name, baudrate=115200)    
    msg = contsruct_payload_from_json(cmd)
    print(f'\nsending: {msg}')        
    s.write(msg)    

if __name__ == '__main__':
    main()
