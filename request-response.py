import signal
from serial import Serial
from utils import contsruct_payload_from_json, get_json_from_packet, PACKET_FOOTER                    

serial_port:Serial = None

def exit_handler(sig, frame):
    global serial_port
    print(f"Signal caught:")
    if serial_port and serial_port.is_open:
        print("    Closing port...")
        serial_port.close()
    quit("    Quitting...")


def main():
    global serial_port
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    # port_name = '/dev/cu.usbmodem101'
    port_name = 'COM11'
    # port_name = '/dev/ttys016'

    serial_port = Serial(port_name, baudrate=115200, timeout=0.2)
    msg = contsruct_payload_from_json('{"command":"get_device_info"}')
    # msg = contsruct_payload_from_json('{"command":"get_sessions", "args": {"limit": 10}}')
    serial_port.write(msg)  

    while True:  
        print('In while loop...')      
        resp_packet = None
        while not resp_packet:            
            resp_packet = serial_port.read_until(PACKET_FOOTER)  
            # print(f"resp_packet: {resp_packet}")          
        resp_json = get_json_from_packet(resp_packet)
        print("Received:", resp_json)      

if __name__ == '__main__':
    main()
