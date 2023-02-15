from serial.tools.list_ports import comports
from serial import Serial
from struct import pack, unpack
from utils import crc8, PACKET_HEADER, PACKET_FOOTER
                        
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

def main():
    port_name = '/dev/ttys016'
    # port_name = '/dev/tty.usbserial-54790373251'

    '''
    The following commands produce a INVALID PACKET RECIEVED error in the API.
    The crc8() function appears to produced the correct crc value
    but the API is not able to match it.
	
    "disconnect" // crc=206, crc.to_bytes=\xce
	"get_wifi_info" // crc=242, crc.to_bytes=\xf2
	"set_wifi" // crc=165, crc.to_bytes=\xa5

    The following commands work BUT they are not producing the correct
    crc value.
	
    "get_commands"  // crc=3, crc.to_bytes=\x03
	"get_sessions"  // crc=93, crc.to_bytes=]
	"get_session"   // crc=126, crc.to_bytes=~
	"get_sample"	// crc=34, crc.to_bytes="
    
    '''

    s = Serial(port_name, baudrate=115200)  
    msg = contsruct_payload_from_json('{"command":"disconect"}')
    print(f'\nsending: {msg}')        
    s.write(msg)    

if __name__ == '__main__':
    main()
