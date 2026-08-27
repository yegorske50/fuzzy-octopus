import isotp
import udsoncan
import udsoncan.configs
from udsoncan.client import Client
from udsoncan.connections import IsoTPSocketConnection

from config import DIDS
from transport import clientaddress, build_isotp_stack

isoconn, udsconfig = build_isotp_stack(clientaddress)

with Client(isoconn, config=udsconfig) as client:
    response = client.read_data_by_identifier(DIDS['vin'])
    print(f"{response.service_data.values[DIDS['vin']]}")