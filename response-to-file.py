from serial     import Serial
from signal     import signal, SIGINT, SIGTERM
from time       import time
from typing     import Final, NoReturn
from utils      import contsruct_payload_from_json, get_json_from_packet, PACKET_HEADER, PACKET_FOOTER

#####################################################################
### User variables. Adjust these to your heart's content.
PORT_NAME:          Final[str]      = 'COM6'
RESPONSE_FILE:      Final[str]      = 'response.txt'    # The output of received responses.
READ_CHUNK_SIZE:    Final[int]      = 1024              # The number of bytes to read at a time.
RESPONSE_TIMEOUT:   Final[float]    = 5.0               # The inter-byte timeout (seconds).

#####################################################################
### Internal variables. DO NOT EDIT UNLESS YOU KNOW WHAT YOU'RE DOING.
_RW_CMD_QUERY:      Final[str]      = 'Command: '
_RW_SERIAL_TIMEOUT: Final[float]    = 0.2
_RW_SERIAL_CONN:    Serial          = None
_RW_DO_EXIT:        bool            = False


def signal_handler(sig, frame) -> None:
    global _RW_DO_EXIT
    _RW_DO_EXIT = True
    print(f'Signal caught: {sig}', flush=True)

def fatal(msg: str) -> NoReturn:
    global _RW_SERIAL_CONN

    print('FATAL: %s' % msg, flush=True)
    if _RW_SERIAL_CONN.is_open:
        _RW_SERIAL_CONN.close()
    quit()

def fatal_bad_header() -> NoReturn:
    fatal('Packet did not start with header')

def fatal_incomplete_response() -> NoReturn:
    global RESPONSE_TIMEOUT
    fatal('Did not receive packet footer for %f seconds' % RESPONSE_TIMEOUT)



def main() -> int:
    global _RW_SERIAL_CONN, PORT_NAME

    signal(SIGINT, signal_handler)
    signal(SIGTERM, signal_handler)


    ### Wipe response file contents.
    with open(RESPONSE_FILE, 'w') as f:
        pass


    ### Open serial port.
    _RW_SERIAL_CONN = Serial(port=PORT_NAME, baudrate=115200, timeout=_RW_SERIAL_TIMEOUT)
    if not _RW_SERIAL_CONN.is_open:
        fatal('Failed to open port')


    ### Write command to API.
    print('Enter a command to send to the API (q to quit).\n'
          'To provide arguments, append a space then the JSON string.\n')
    while not _RW_DO_EXIT:
        user_input: str = input(_RW_CMD_QUERY)
        if user_input.lower() == 'q':
            break

        parts = user_input.split(sep=' ')
        cmd = parts[0]
        if len(parts) > 1:
            args = ''.join(parts[1:])
        else:
            args = ''


        json_req: str   = '{ "command":"%s", "args": %s }' % (cmd, args)
        payload: bytes  = contsruct_payload_from_json(json_req, do_print=False)
        _RW_SERIAL_CONN.write(payload)


        ### Read serial data in chunks of size `CHUNK_SIZE`.
        received: bytes = b''
        n_recvs: int = 0
        has_valid_header: bool = False
        last_recv_time: float = None

        while not _RW_DO_EXIT:
            # Read a chunk of available data.
            try: buf: bytes = _RW_SERIAL_CONN.read(READ_CHUNK_SIZE)
            except Exception as e:
                print(e, flush=True)
                quit()
        
            # We timed out.
            if len(buf) == 0:
                # If we've received ANY data, check for response timeout...
                if last_recv_time is not None:
                    if time() - last_recv_time > RESPONSE_TIMEOUT:
                        fatal_incomplete_response()
                continue
            
            # Data was available!
            else:
                last_recv_time = time()
                n_recvs += 1
                print('read: (#%lu) +%lu total[%lu]' % (n_recvs, len(buf), len(received)), flush=True)

            # Ensure valid packet header.
            if not has_valid_header: # and len(received) < len(PACKET_HEADER):
                if len(received) == 0:
                    if len(buf) == 1:
                        if buf[0] != PACKET_HEADER[0]:
                            fatal_bad_header()
                    else: # len(buf) MUST be > 1
                        if buf.startswith(PACKET_HEADER):
                            has_valid_header = True
                        else:
                            fatal_bad_header()
                else: # len(received) MUST be == 1
                    if buf[0] == PACKET_HEADER[1]:
                        has_valid_header = True
                    else:
                        fatal_bad_header()
            
            # Append data and check for packet footer.
            received += buf
            if has_valid_header and PACKET_FOOTER in received:
                if received.endswith(PACKET_FOOTER):
                    print('Packet ended with proper footer! (packet length = %lu)' % len(received))
                    break
                else:
                    idx = received.find(PACKET_FOOTER)
                    if PACKET_HEADER in received[idx:]:
                        fatal('End of one packet and the start of another were read in the same call')
                    else:
                        fatal('Packet footer not at end of available data.')


        ### Write received JSON to file.
        if not _RW_DO_EXIT:
            json_resp = get_json_from_packet(received, do_print=True)
            if json_resp is None:
                json_resp = 'BAD JSON:\n' + received[6:-3].decode()
            with open(RESPONSE_FILE, 'a') as f:
                f.write(json_resp + '\n')
        

    ### Script done.
    if _RW_SERIAL_CONN.is_open:
        _RW_SERIAL_CONN.close()

    return 0

if __name__ == '__main__':
    code = main()
    print('Done', flush=True)
    quit(code)