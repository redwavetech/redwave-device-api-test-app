from serial.tools.list_ports import comports
from serial import Serial

def main():
    ports = comports()
    for p in ports:
        print(p)
    quit()   

if __name__ == '__main__':
    main()
