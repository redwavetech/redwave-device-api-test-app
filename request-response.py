from serial     import Serial
from signal     import signal, SIGINT, SIGTERM
from time       import time, sleep
from threading  import Thread
from typing     import NoReturn, Final, LiteralString
from utils      import contsruct_payload_from_json, get_json_from_packet, KeyAsyncReader, PACKET_HEADER, PACKET_FOOTER
import threading
#####################################################################
### Internal variables
_RW_CMD_QUERY     : Final[LiteralString] = 'Enter a command name to run: '
_RW_SERIAL_CONN   : Serial = None
_RW_READER_THREAD : Thread = None
_RW_KEEP_ALIVE    : bool   = True
_RW_DO_EXIT       : bool   = False
_RW_INPUT_BUFFER  : str    = ''

#####################################################################
### User variables
IS_INTERCEPTIR : Final[bool] = True
PORT_NAME      : Final[str]  = 'COM8' #'/dev/cu.usbmodem2101' #'/dev/ttys016'



#####################################################################
### Funcs

def exit_handler( sig, frame ) -> None:
    global _RW_DO_EXIT

    print( f'Signal caught: {sig}' )
    _RW_DO_EXIT = True

def keyPressCb( char:str ):
    global _RW_INPUT_BUFFER

    byte:Final[bytes] = char.encode()
    # print( 'Key Pressed:', byte )


    # Backspace
    if ( byte == b'\x08' ) and ( len(_RW_INPUT_BUFFER) > 0 ):
        _RW_INPUT_BUFFER = _RW_INPUT_BUFFER[:-1]
        updateCmdQueryLine()
    
    # Enter
    elif byte == b'\r' or byte == b'\n':
        writeSerialCommand( _RW_INPUT_BUFFER )
        _RW_INPUT_BUFFER = ''
        print()
        updateCmdQueryLine()
        sleep( 0.25 )
    
    # [a-zA-Z_]
    elif byte.isalpha() or byte == b'_':
        _RW_INPUT_BUFFER += char
        updateCmdQueryLine()

def clearCmdQueryLine():
    global _RW_CMD_QUERY, _RW_INPUT_BUFFER

    print( '\r' + (' ' * (len(_RW_CMD_QUERY) + len(_RW_INPUT_BUFFER) + 1)), end='' )

def updateCmdQueryLine():
    global _RW_CMD_QUERY, _RW_INPUT_BUFFER

    newLine:Final[str] = f'{_RW_CMD_QUERY}{_RW_INPUT_BUFFER}'
    
    out:str = '\r'
    out += ' ' * ( len(newLine) + 1 )
    out += f'\r{newLine}'

    print( out, end='' )

def openSerial( port_name: str ) -> None:
    global _RW_SERIAL_CONN

    _RW_SERIAL_CONN = Serial( port_name, baudrate=115200, timeout=0.2 )

def closeSerial() -> None:
    global _RW_SERIAL_CONN

    if _RW_SERIAL_CONN and _RW_SERIAL_CONN.is_open:
        print( 'Closing serial connection...' )
        _RW_SERIAL_CONN.close()

def wait_for_app():
    # Decided to give user 1/2s interval feedback that script is still running
    wait_str : Final[LiteralString] = 'Waiting for app and API to load. Please wait... '
    start    : Final[float]         = time()
    cutoff   : int                  = -3
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

def readSerial() -> str|None:
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
    return get_json_from_packet( buffer )

def writeSerialCommand( cmd: str ) -> int|None:
    global _RW_SERIAL_CONN

    payload:Final[bytes] = contsruct_payload_from_json( '{\"command\":\"' + cmd + '\"}' )
    return _RW_SERIAL_CONN.write( payload )

# The program is stopped when any of the following cases occur:
#   1.  Entering ctrl+c from the console (Expected means of termination)
#   2.  IS_INTERCEPTIR is true and the API mode request packet is not received
def main() -> NoReturn:
    global _RW_SERIAL_CONN, PORT_NAME, _RW_READER_THREAD, _RW_KEEP_ALIVE

    signal( SIGINT, exit_handler )
    signal( SIGTERM, exit_handler )
    json:str|None = None

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
                if _RW_DO_EXIT:
                    closeSerial()
                    return 0

        # Wait for API mode request
        print( 'Waiting for API mode request...' )
        json = readSerial()

        if _RW_DO_EXIT:
            closeSerial()
            return 0
        elif json == '{"request":"which_mode"}':
            # Choose USB mode
            _RW_SERIAL_CONN.write( contsruct_payload_from_json('{"mode":"usb"}', do_print=True) )
            print( 'Selecting USB API mode...' )
        else:
            print( f'Expected API mode request but instead received: "{json}"\nQuitting...' )
            closeSerial()
            return 1

        # Give the app and API time to load...
        # print( 'Waiting for app and API to load. Please wait...' )
        # sleep( 60.0 )
        wait_for_app()
    else:
        openSerial( PORT_NAME )



    #################    
    # Notice - we updated our API since this program was created.  The new API has several 
    # long-running commands, like start_cm, that continually return responses which this 
    # program may not be suited for.  For now, it's recommended to stick with single-response 
    # commands like "get_device_info". In the future, we plan to have more single-response
    # commands that can be used with this script. 
    #################
    
    # Start keystroke-capture thread
    keycap = KeyAsyncReader()
    keycap.startReading( keyPressCb )
    
    print( 'Getting device info...' )
    writeSerialCommand( 'get_device_info' )

    # Main program loop
    while not _RW_DO_EXIT:  
        json = readSerial()
        if json:
            clearCmdQueryLine()
            print( f'\rReceived:\n{json}' )
            updateCmdQueryLine()

    # Join keystroke-capture thread
    keycap.stopReading()

    # Close serial connection
    closeSerial()
    
    return 0


#####################################################################
### Script entry point
if __name__ == '__main__':
    main()
