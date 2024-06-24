from serial.tools.list_ports import comports
from serial import Serial
from time       import time, sleep

def main():
    while True:
        ports = comports()
        for port, desc, hwid in ports:
            print(f'port={port}, desc={desc}, hwid={hwid}')                    
        print('\n- - - - - - - - - - - -\n')
        sleep(1)

if __name__ == '__main__':
    main()
