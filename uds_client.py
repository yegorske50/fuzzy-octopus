import isotp
import udsoncan
import udsoncan.configs
from udsoncan.client import Client
from udsoncan.connections import IsoTPSocketConnection

from config import DIDS
from transport import clientaddress, build_isotp_stack

def read_did(client, name):
    did = DIDS[name]
    response = client.read_data_by_identifier(did)
    return response.service_data.values[did]

