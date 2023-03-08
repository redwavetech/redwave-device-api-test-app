from struct import pack, unpack

PACKET_HEADER = b'\x01\x02'
PACKET_FOOTER = b'\x03\x04'

def crc8(payload:bytes):
    crc = 0
    mix = 0    
    for inbyte in payload:        
        for i in range(8):
            mix = (crc ^ inbyte) & 1
            crc >>= 1
            if mix:                
                crc ^= 0x8c                
            inbyte >>= 1    
    return crc

def get_json_from_packet(packet:bytes):
    
    # Check packet header
    if packet[:2] != PACKET_HEADER:                     
        raise Warning("INVALID PACKET HEADER")
    # print(f'packet header: {packet[:2]}')        

    json_supposed_len, = unpack('<I', packet[2:6]) 
    # print(f'packet length: {packet[2:6]}')
        
    # Extract JSON message
    json_bytes = packet[6:-3]
    json_str = json_bytes.decode()                           
    # print(f'packet json: {json_str}')
    
    # Extract alleged length of JSON message 
    # (interpret bytes as an unsigned integer)
    if (json_supposed_len != len(json_bytes)):
        raise Warning("MESSAGE LENGTH MISMATCH")
    
    # Extract CRC
    crc = packet[-3] 
    crc_packet = packet[-3:-2]                                  
    # print(f'packet crc: {crc_packet}')
    if (crc != crc8(json_bytes)):
        raise Warning("CRC MISMATCH")
    
    # Check packet footer
    packet_footer = packet[-2:]
    if packet_footer != PACKET_FOOTER:                    
        raise Warning("INVALID PACKET FOOTER")    
    # print(f'packet footer: {packet_footer}')
            
    return json_str

def contsruct_payload_from_json(json_str:str):

    json_bytes = json_str.encode()                      # Convert string to bytes
    crc = crc8(json_bytes)

    print('- - - - Request from app - - - - -') 
    print(f'packet header: {PACKET_HEADER}')    
    print(f'packet length: {pack("<I", len(json_str))}')
    print(f'packet json: {json_bytes}')
    print(f'packet crc: bytes={crc.to_bytes(1, "little", signed=False)}, int={crc}')
    # print(f'packet crc.to_bytes, {crc.to_bytes(1, "little")}')
    print(f'packet footer: {PACKET_FOOTER}')    

    return b''.join([
        PACKET_HEADER,
        pack("<I", len(json_str)),                      # Convert length to unsigned integer byte representation        
        json_bytes,
        crc.to_bytes(1, 'little', signed=False),        # Convert CRC to byte representation
        PACKET_FOOTER
    ])