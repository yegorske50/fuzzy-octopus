import isotp
import config
from config import DIDS
from transport import ecuaddress

DID_VALUE = b"LEARNUDS"


tpsock = isotp.socket()
tpsock.bind(config.CAN_INTERFACE, ecuaddress)

print(f"ECU simulator up on {config.CAN_INTERFACE}")

while True:
    request = tpsock.recv()

    if request[:3] == bytes([0x22, DIDS['vin'] >> 8, DIDS['vin'] & 0xFF]):

        response = bytes([0x62, DIDS['vin'] >> 8, DIDS['vin'] & 0xFF]) + DID_VALUE
        tpsock.send(response)
        print(f"-> ReadDataByIdentifier replied {DID_VALUE}")