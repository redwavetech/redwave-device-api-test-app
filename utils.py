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