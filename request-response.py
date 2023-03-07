from serial import Serial
from utils import contsruct_payload_from_json, get_json_from_packet, PACKET_FOOTER                    

def main():
    port_name = '/dev/ttys016'
    # port_name = '/dev/tty.usbserial-54790373251'

    s = Serial(port_name, baudrate=115200)
    msg = contsruct_payload_from_json('{"command":"get_commands"}')
    s.write(msg)

    resp_packet = s.read_until(PACKET_FOOTER)
    resp_json = get_json_from_packet(resp_packet)
    print("Received:", resp_json)    

if __name__ == '__main__':
    main()
