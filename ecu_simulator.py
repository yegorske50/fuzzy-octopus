import isotp
import config
from config import DIDS
from transport import ecuaddress
from udsoncan import Response
from udsoncan import services
import random
import time

# reverse dict of DIDS for 
DID_NAMES = {did: name for name, did in DIDS.items()}

ecu_state = {
    "vin": None,
    "csr": None,
    "device_id": None,
    "vin_alias": None,
    "device_cert": None,
    "session": services.DiagnosticSessionControl.Session.defaultSession,
}

class SendNegativeResponse(Exception):
    def __init__(self, service_id, nrc):
        self.service_id = service_id
        self.nrc = nrc

def generate_csr(vin):
    random.seed(vin)
    length = random.randint(600, 900)
    return "CSR-FOR-" + vin + "-" + ("A" * length)

####################### Actions ##############################

def read_did(request):
    did = int.from_bytes(request[1:3], "big")
    did_name = DID_NAMES.get(did)

    if did_name is None or ecu_state.get(did_name) is None:
        raise SendNegativeResponse(service_id=0x22, nrc=Response.Code.RequestOutOfRange)

    return  bytes([0x62]) + request[1:3] + ecu_state.get(did_name).encode("utf-8")

def write_did(request):
    did = int.from_bytes(request[1:3], "big")
    did_name = DID_NAMES.get(did)

    if did_name is None:
        raise SendNegativeResponse(service_id=0x2E, nrc=Response.Code.RequestOutOfRange)

    value = request[3:].decode("utf-8")
    ecu_state[did_name] = value

    if did_name == 'vin':
        ecu_state["csr"] = generate_csr(value)
    
    return bytes([0x6E]) + request[1:3]

def session_control(request):
    session_type = request[1]

    if session_type not in [services.DiagnosticSessionControl.Session.defaultSession, services.DiagnosticSessionControl.Session.extendedDiagnosticSession]:
        raise SendNegativeResponse(service_id=0x10, nrc=Response.Code.SubFunctionNotSupported)
    
    ecu_state["session"] = session_type
    return bytes([0x50, session_type, 0x01, 0xF4, 0x01, 0xF4]) # p2(500ms) and p2*(5s - since it is in terms of 10ms) of server.

def tester_present(request):
    # to implement when no reponse is handled in the main loop
    # if request[1] == 0x80:
    #     return None
    return bytes([0x7E, request[1]])

def ecu_reset(request):
    reset_type = request[1]
    if reset_type not in [services.ECUReset.ResetType.hardReset, services.ECUReset.ResetType.softReset]:
        raise SendNegativeResponse(service_id=0x11, nrc=Response.Code.SubFunctionNotSupported)
    return bytes([0x51, reset_type])

def routine_control(request):
    control_type = request[1]
    routine_id = int.from_bytes(request[2:4], "big")
    if routine_id != config.ROUTINES["verify_certificate_integrity"]:
        raise SendNegativeResponse(service_id=0x31, nrc=Response.Code.RequestOutOfRange)
    # do nothing currently, just return positive response
    return bytes([0x71, control_type]) + request[2:4]

#####################################################

# sid and function mapping
DISPATCH = {
    0x22: read_did,
    0x2E: write_did,
    0x10: session_control,
    0x3E: tester_present,
    0x11: ecu_reset,
    0x31: routine_control,
}

tpsock = isotp.socket()
tpsock.bind(config.CAN_INTERFACE, ecuaddress)

print(f"ECU simulator up on {config.CAN_INTERFACE}")

while True:
    request = tpsock.recv()

    sid = request[0]

    try:
        handler = DISPATCH.get(sid)
        if handler is None:
            raise SendNegativeResponse(service_id=sid, nrc=Response.Code.ServiceNotSupported)
        response = handler(request)
    except SendNegativeResponse as e:
        response = bytes([0x7F, e.service_id, e.nrc.value])
        print(f"-> Sending negative response: {response.hex()}")

    tpsock.send(response)
    print(f"sending response {response.hex()}")


    if sid == 0x11 and response[0] != 0x7F:
        ecu_state["session"] = services.DiagnosticSessionControl.Session.defaultSession
        print("Simulating ECU reboot (5s)...")
        time.sleep(5)
        print("ECU back online") 