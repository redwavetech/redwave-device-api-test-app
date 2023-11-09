from serial     import Serial
from signal     import signal, SIGINT, SIGTERM
import sys
from time       import time, sleep
from typing     import Final
from utils_mac  import contsruct_payload_from_json, get_json_from_packet, PACKET_HEADER, PACKET_FOOTER
from serial.tools.list_ports import comports

_RW_DO_EXIT     = False
_RW_SERIAL_CONN : Serial = None

IS_INTERCEPTIR  = True
PORT_DESCRIPTION = 'Gadget Serial'
PORT_NAME       = None

def exit_handler( sig, frame ) -> None:
    global _RW_DO_EXIT

    print( f'Signal caught: {sig}' )
    _RW_DO_EXIT = True        
    sys.exit(0)

def openSerial():
    global PORT_NAME, _RW_SERIAL_CONN    
    _RW_SERIAL_CONN = Serial(
        PORT_NAME, 
        baudrate=115200,
        timeout=None
    )

def closeSerial() -> None:
    global _RW_SERIAL_CONN

    if _RW_SERIAL_CONN and _RW_SERIAL_CONN.is_open:
        print( 'Closing serial connection...' )
        _RW_SERIAL_CONN.close()

def readSerial():
    global _RW_SERIAL_CONN, _RW_DO_EXIT
    buffer:bytes = b''
    timeFirstByte = None

    # Local function for handling invalid packet structure
    def _readError( msg: str ):
        print( msg )
        _RW_SERIAL_CONN.read_all() # flush read buffer


    # Read serial buffer one byte at a time.
    # We explicitly AVOID use of `Serial.read_until(...)` due to existing bug(s) which lead to undefined behavior.
    while not _RW_DO_EXIT:

        # Read one byte
        byte:bytes = _RW_SERIAL_CONN.read( 1 ) # 0.2s timeout (set upon Serial obj construction)
        
        # If read timed out, read again
        if len( byte ) == 0:
            continue
        
        # Ensure first two bytes are the packet header
        elif ( buffer == b'' ) and ( byte != PACKET_HEADER[0].to_bytes(1, "little", signed=False) ): # Accessing an array of bytes by index returns an int, so we re-cast to bytes for comparison
            _readError( f'FIRST BYTE WAS {byte}, NOT {PACKET_HEADER[0].to_bytes(1, "little", signed=False)}' )
            return None
        elif ( buffer == PACKET_HEADER[0].to_bytes(1, "little", signed=False) ) and ( byte != PACKET_HEADER[1].to_bytes(1, "little", signed=False) ):
            _readError( f'SECOND BYTE WAS {byte}, NOT {PACKET_HEADER[1].to_bytes(1, "little", signed=False)}' )
            return None
        


        # Append byte to packet buffer
        buffer += byte

        # If the packet has taken longer than 2 seconds to receive, consider it invalid and exit loop
        if timeFirstByte == None:
            timeFirstByte = time()
        elif time() - timeFirstByte > 3.0:
            _readError( 'PACKET STILL INCOMPLETE AFTER 3.0 SECONDS' )
            return None
        
        # If we've received the packet footer, stop reading
        elif buffer.endswith( PACKET_FOOTER ):
            break
    
    if _RW_DO_EXIT:
        return None
    
    # Parse JSON message from packet
    return get_json_from_packet( buffer, do_print=False )

def wait_for_app():
    print('wait_for_app')
    # Decided to give user 1/2s interval feedback that script is still running
    wait_str    = 'Waiting for app and API to load. Please wait... '
    start       : Final[float]         = time()
    cutoff      : int                  = -3
    while True:
        print( ' ' * len(wait_str), end='\r' )  # erase line
        print( wait_str[:cutoff], end='\r' )    # update line
        sleep( 0.5 )
        if _RW_DO_EXIT:
            closeSerial()
            return 0
        elif time() - start >= 60.0:
            print() # newline
            break
        elif cutoff == -1:
            cutoff = -3
        else:
            cutoff += 1

def main():  
    global PORT_NAME
    print('main')
    signal( SIGINT, exit_handler )
    signal( SIGTERM, exit_handler )
    json:str|None = None

    
    while PORT_NAME is None:
        ports = comports()
        for port, desc, hwid in ports:            
            if PORT_DESCRIPTION in desc:
                PORT_NAME = port                
                break                                        
        sleep(0.5)
        print('Waiting for port information...')

    
    if IS_INTERCEPTIR:
        print( 'Waiting for InterceptIR to open serial connection...' )

        # Wait for IIR to open serial port.
        # Once open, do not send any commands but instead listen for API mode request
        while True:
            try:
                openSerial()
                break
            except IOError as e:
                continue

        # Wait for API mode request
        print( 'Waiting for API mode request...' )
        json = readSerial()

        if _RW_DO_EXIT:
            closeSerial()
            return 0
        elif json == '{"request":"which_mode"}':
            # Choose USB mode
            _RW_SERIAL_CONN.write( contsruct_payload_from_json('{"mode":"usb"}') )
            print( 'Selecting USB API mode...' )
        else:
            print( f'Expected API mode request but instead received: "{json}"\nQuitting...' )
            closeSerial()
            return 1

        # # Give the app and API time to load...
        # # print( 'Waiting for app and API to load. Please wait...' )        
        wait_for_app()
    else:        
        openSerial()  

    if _RW_SERIAL_CONN == None:    
        print('Could not open port')
        return False
    
    print('Ready to receive API commands...')
        
    while True:     
        if _RW_SERIAL_CONN.in_waiting > 0:               
            resp_packet = _RW_SERIAL_CONN.read_until(PACKET_FOOTER) 
            print('- - - Response from API - - -')           
            print(f'packet (raw): {resp_packet}')
            print('- - - - - - - - - -')
            resp_json = get_json_from_packet(resp_packet)  
            print(resp_json)                    

if __name__ == '__main__':
    main()
