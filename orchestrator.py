# import logging
import time

import udsoncan
from udsoncan.client import Client

import config
import transport
import uds_client as udsc
from transport import clientaddress, build_isotp_stack

# logging.basicConfig(level=logging.INFO)
# log = logging.getLogger("provision")

def _retry_until_success(operation, max_attempts=10, delay=1.0):
    for attempt in range(1, max_attempts + 1):
        try:
            return operation()
        except udsoncan.exceptions.TimeoutException as e:
            print(f"Attempt {attempt}/{max_attempts}: ECU not responding yet ({e})")
            time.sleep(delay)
    raise RuntimeError("ECU did not come back after reset")

def flow(vin):
    isoconn, udsconfig = build_isotp_stack(clientaddress)

    with Client(isoconn, config=udsconfig) as client:
        try:
            udsc.enter_extended_session(client)
            udsc.write_did(client, 'vin', vin)
            csr = udsc.read_did(client, 'csr')
        except udsoncan.exceptions.NegativeResponseException as e:
            print(f"ECU rejected programming vin or providing csr: {e}")
            return

        try:
            creds = ca_client.get_signed_cert(csr)
        except ca_client.CloudApiError as e:
            print(f"Cloud API call failed: {e}")
            return

        try:
            udsc.write_did(client, 'device_id', creds['device_id'])
            udsc.write_did(client, 'vin_alias', creds['vin_alias'])
            udsc.write_did(client, 'device_certificate', creds['device_certificate'])
            udsc.ecu_reset(client)
            udsc.enter_extended_session(client)
        except udsoncan.exceptions.NegativeResponseException as e:
            print(f"ECU rejected credential programming or reset: {e}")
            return

        try:
            _retry_until_success(lambda: udsc.verify_integrity(client))
        except RuntimeError as e:
            print(f"{e}")
            return

    print("Provisioning complete")


if __name__ == "__main__":
    flow("NEWVIN1234567890")
