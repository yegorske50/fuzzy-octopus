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

        try:
            response = udsc.read_did(client, 'csr')
            print(f"{response}")
        except Exception as e:
            print(f"Error: {e}")

        # udsc.write_did(client, 'vin', 'NEWVIN1234567890')


if __name__ == "__main__":
    flow()
