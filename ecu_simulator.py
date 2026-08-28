import isotp
import config
from config import DIDS
from transport import ecuaddress
from udsoncan import Response
import random

DID_VALUE = b"LEARNUDS"

ecu_state = {
    "vin": None,
    "csr": "ccllaajj",
}

class SendNegativeResponse(Exception):
    def __init__(self, service_id, nrc):
        self.service_id = service_id
        self.nrc = nrc

def read_did(request):
    did = int.from_bytes(request[1:3], "big")
    if did == DIDS["csr"]:
        return  bytes([0x62]) + request[1:3] + ecu_state["csr"].encode("utf-8")

    raise SendNegativeResponse(service_id=0x22, nrc=Response.Code.RequestOutOfRange)

def write_did(request):
    did = int.from_bytes(request[1:3], "big")
    vinvalue = request[3:].decode("utf-8")

    if did == DIDS["vin"]:
        ecu_state["vin"] = vinvalue
        ecu_state["csr"] = generate_csr(vinvalue)
        return bytes([0x6E]) + request[1:3]

    raise SendNegativeResponse(service_id=0x2E, nrc=Response.Code.RequestOutOfRange)


def generate_csr(vin):
    random.seed(vin)
    length = random.randint(600, 900)
    return "CSR-FOR-" + vin + "-" + ("A" * length)

print(f"ECU simulator up on {config.CAN_INTERFACE}")

tpsock = isotp.socket()
tpsock.bind(config.CAN_INTERFACE, ecuaddress)

while True:
    request = tpsock.recv()

    try:
        if request[0:1] == bytes([0x22]):
            response = read_did(request)
        elif request[0:1] == bytes([0x2E]):
            response = write_did(request)
        else:
            raise SendNegativeResponse(service_id=request[0], nrc=Response.Code.ServiceNotSupported)
    except SendNegativeResponse as e:
        response = bytes([0x7F, e.service_id, e.nrc.value])
        print(f"-> Sending negative response: {response}")

    tpsock.send(response)
    print(f"sending response {response.hex()}")
