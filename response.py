import serial
from utils import get_json_from_packet, PACKET_HEADER, PACKET_FOOTER

def main():    

    port_name = '/dev/cu.usbmodem2101'    
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
            print('- - - - - - - - - -')
            resp_json = get_json_from_packet(resp_packet)  
            print(resp_json)                    

if __name__ == '__main__':
    main()
