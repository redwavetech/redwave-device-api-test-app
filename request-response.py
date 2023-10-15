# import argparse
from serial import Serial
import signal
from utils import contsruct_payload_from_json, get_json_from_packet, PACKET_FOOTER
from time import sleep
import time
# from json import loads as jsonStrToDict
serial_port:Serial = None

#####################################################################
### User variables
                   
IS_INTERCEPTIR:bool = True

# PORT_NAME:str = '/dev/cu.usbmodem2101'
PORT_NAME:str = 'COM8'
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
    resp_packet:bytes = b''

    while (not resp_packet.endswith( PACKET_FOOTER )) or (len(resp_packet) == 0):
        resp_packet = serial_port.read_until( PACKET_FOOTER ) # timeout of 0.2s
    
    resp_json = get_json_from_packet( resp_packet )
    print( "Received:", resp_json )
    return resp_json

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
        mystr = 'Waiting for app and API to load. Please wait... ' # trailing charater required
        cutoff = -3
        start = time.time()
        while True: # decided to give user 1/2s interval feedback that script is still running
            print( ' ' * len(mystr), end='\r' )
            print( mystr[:cutoff], end='\r' )
            sleep( 0.5 )
            if time.time() - start >= 60.0:
                break
            elif cutoff == -1:
                cutoff = -3
            else:
                cutoff += 1
        print() # newline
    else:
        openSerial(PORT_NAME)

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
