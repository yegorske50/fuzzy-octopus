import logging
from udsoncan.client import Client
import config
import transport
import uds_client as udsc
from transport import clientaddress, build_isotp_stack

# logging.basicConfig(level=logging.INFO)
# log = logging.getLogger("provision")

def flow():
    isoconn, udsconfig = build_isotp_stack(clientaddress)

    with Client(isoconn, config=udsconfig) as client:
        response = udsc.read_did(client, 'vin')
        print(f"{response}")


if __name__ == "__main__":
    flow()
