# import argparse
from serial import Serial
import signal
from utils import contsruct_payload_from_json, get_json_from_packet, PACKET_HEADER, PACKET_FOOTER
from time import sleep
import time
# from json import loads as jsonStrToDict
serial_port:Serial = None

#####################################################################
### User variables
                   
IS_INTERCEPTIR:bool = False

# PORT_NAME:str = '/dev/cu.usbmodem2101'
PORT_NAME:str = 'COM5'
# PORT_NAME:str = '/dev/ttys016'




#####################################################################
### Funcs

def exit_handler(sig, frame):
    global serial_port

    print(f"Signal caught:")
    if serial_port and serial_port.is_open:
        print("    Closing port...")
        serial_port.close()
    
    quit("    Quitting...")

def openSerial( port_name: str ) -> None:
    global serial_port
    serial_port = Serial( port_name, baudrate=115200, timeout=0.2 )

def readSerial() -> str|None:
    global serial_port
    buffer:bytes = b''
    timeFirstByte = None

    # Local function for handling invalid packet structure
    def _readError( msg: str ):
        print( msg )
        serial_port.read_all() # flush read buffer


    # Read serial buffer one byte at a time.
    # We explicitly AVOID use of `Serial.read_until(...)` due to existing bug(s) which lead to undefined behavior.
    while True:

        # Read one byte
        byte:bytes = serial_port.read( 1 ) # 0.2s timeout (set upon Serial obj construction)
        
        # If read timed out, read again
        if len( byte ) == 0:
            continue
        
        # Ensure first two bytes are the packet header
        elif ( buffer == b'' ) and ( byte != PACKET_HEADER[0].to_bytes() ): # Accessing an array of bytes by index returns an int, so we re-cast to bytes for comparison
            _readError( f'FIRST BYTE WAS {byte}, NOT {PACKET_HEADER[0].to_bytes()}' )
            return None
        elif ( buffer == PACKET_HEADER[0].to_bytes() ) and ( byte != PACKET_HEADER[1].to_bytes() ):
            _readError( f'SECOND BYTE WAS {byte}, NOT {PACKET_HEADER[1].to_bytes()}' )
            return None
        


        # Append byte to packet buffer
        buffer += byte

        # If the packet has taken longer than 2 seconds to receive, consider it invalid and exit loop
        if timeFirstByte == None:
            timeFirstByte = time.time()
        elif time.time() - timeFirstByte > 2.0:
            _readError( 'PACKET STILL INCOMPLETE AFTER 2.0 SECONDS' )
            return None
        
        # If we've received the packet footer, stop reading
        elif buffer.endswith( PACKET_FOOTER ):
            break
    
    
    # Parse JSON message from packet
    json_str = get_json_from_packet( buffer )
    if json_str == None:
        print( 'Failed to parse packet.' )
    else:
        print( 'Received:', json_str )

    return json_str

def writeSerialCommand( cmd: str ):
    global serial_port
    payload = contsruct_payload_from_json( '{\"command\":\"' + cmd + '\"}' )
    serial_port.write( payload )

def main():
    global serial_port, PORT_NAME
    signal.signal(signal.SIGINT, exit_handler)
    signal.signal(signal.SIGTERM, exit_handler)

    # parser=argparse.ArgumentParser()
    # parser.add_argument("--command", help="Must be a valid command, like: get_device_info, start_cm, cancel_cm, etc.")  
    # args=parser.parse_args()
    # cmd = args.command    
    # print(f'Sending command: {cmd}')

    if IS_INTERCEPTIR:
        print( 'Waiting for InterceptIR to open serial connection...' )

        # Wait for IIR to open serial port.
        # Once open, do not send any commands but instead listen for API mode request
        while True:
            try:
                openSerial( PORT_NAME )
                break
            except IOError as e:
                # print( e.args[0] )
                pass
        
        # Wait for API mode request
        print( 'Waiting for API mode request...' )
        json = readSerial()

        if json == '{"request":"which_mode"}':
            # Choose USB mode
            serial_port.write( contsruct_payload_from_json('{"mode":"usb"}') )
            print( 'Selecting USB API mode...' )
        else:
            print( f'Expected API mode request but instead received: "{json}"\nQuitting...' )
            if serial_port and serial_port.is_open:
                serial_port.close()
            exit( 1 )

        # Give the app and API time to load...
        # print( 'Waiting for app and API to load. Please wait...' )
        # sleep( 60.0 )

        # Decided to give user 1/2s interval feedback that script is still running
        wait_str = 'Waiting for app and API to load. Please wait... '
        cutoff = -3
        start = time.time()
        while True:
            print( ' ' * len(wait_str), end='\r' )  # erase line
            print( wait_str[:cutoff], end='\r' )    # update line
            sleep( 0.5 )
            if time.time() - start >= 60.0:
                break
            elif cutoff == -1:
                cutoff = -3
            else:
                cutoff += 1
        print() # newline
    else:
        openSerial( PORT_NAME )

    #################    
    # Notice - we updated our API since this program was created.  The new API has several 
    # long-running commands, like start_cm, that continually return responses which this 
    # program may not be suited for.  For now, it's recommended to stick with single-response 
    # commands like "get_device_info". In the future, we plan to have more single-response
    # commands that can be used with this script. 
    #################
    
    print( 'Getting device info...' )
    writeSerialCommand( 'get_device_info' )

    while True:  
        # print('In while loop...')
        
        resp_json_str = readSerial()
        if IS_INTERCEPTIR:
            cmd = input( 'Enter a command name to run: ' )
            writeSerialCommand( cmd )

    # serial_port.close()



#####################################################################
### Script entry point
if __name__ == '__main__':
    main()
