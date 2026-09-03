# import isotp
import udsoncan
# import udsoncan.configs
# from udsoncan.client import Client
# from udsoncan.connections import IsoTPSocketConnection
from udsoncan import services
import config
from config import DIDS
# from transport import clientaddress, build_isotp_stack

import time

def read_did(client, name):
    did = DIDS[name]
    response = client.read_data_by_identifier(did)
    return response.service_data.values[did]

def write_did(client, name, value):
    did = DIDS[name]
    client.write_data_by_identifier(did, value)

def enter_extended_diagnostic_session(client):
    client.change_session(services.DiagnosticSessionControl.Session.extendedDiagnosticSession)

def ecu_reset(client):
    client.ecu_reset(services.ECUReset.ResetType.hardReset)
    time.sleep(1.0)  

def verify_integrity(client):
    routine_id = config.ROUTINES["verify_certificate_integrity"]
    client.start_routine(routine_id)

def send_tester_present(client):
    client.tester_present()

# take care of errors to be caught