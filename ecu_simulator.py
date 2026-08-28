import isotp
import config
from config import DIDS
from transport import ecuaddress

DID_VALUE = b"LEARNUDS"


tpsock = isotp.socket()
tpsock.bind(config.CAN_INTERFACE, ecuaddress)

ecu_state = {
    "vin": None,
    "csr": "ccllaajj",
}

def read_did(request):
    did = int.from_bytes(request[1:3], "big")
    if did == DIDS["csr"]:
        response = bytes([0x62]) + request[1:3] + ecu_state["csr"].encode("utf-8")

    return response

print(f"ECU simulator up on {config.CAN_INTERFACE}")

while True:
    request = tpsock.recv()

    if request[0:1] == bytes([0x22]):
        response = read_did(request)
        tpsock.send(response)
        print(f"-> ReadDataByIdentifier replied {response[3:].decode('utf-8')}")

    # if request[0:1] == bytes([0x22]) and request[1:3] == DIDS["vin"].to_bytes(2, "big"):
    #     response = bytes([0x62]) + request[1:3] + DID_VALUE
    #     tpsock.send(response)
    #     print(f"-> ReadDataByIdentifier replied {DID_VALUE}")

    # if request[:3] == bytes([0x22, DIDS['vin'] >> 8, DIDS['vin'] & 0xFF]):

    #     response = bytes([0x62, DIDS['vin'] >> 8, DIDS['vin'] & 0xFF]) + DID_VALUE
    #     tpsock.send(response)
    #     print(f"-> ReadDataByIdentifier replied {DID_VALUE}")

