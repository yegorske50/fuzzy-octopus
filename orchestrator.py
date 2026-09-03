# import logging
import time

import udsoncan
from udsoncan.client import Client

import config
import transport
import uds_client as udsc
from transport import clientaddress, build_isotp_stack
from utils import retry_until_success, retry_with_backoff
import cloud_client

# logging.basicConfig(level=logging.INFO)
# log = logging.getLogger("provision")


def flow(vin):
    isoconn, udsconfig = build_isotp_stack(clientaddress)

    with Client(isoconn, config=udsconfig) as client:

        try:
            udsc.enter_extended_diagnostic_session(client)
        except RuntimeError as e:
            print(f"{e}")
            return

        try:
            udsc.write_did(client, 'vin', vin)
            csr = udsc.read_did(client, 'csr')
        except udsoncan.exceptions.NegativeResponseException as e:
            print(f"ECU rejected programming vin or providing csr: {e}")
            return

        # to be implemented
        creds = cloud_client.get_cert(csr)

        try:
            udsc.write_did(client, 'device_id', creds['device_id'])
            udsc.write_did(client, 'vin_alias', creds['vin_alias'])
            udsc.write_did(client, 'device_cert', creds['device_cert'])
            udsc.ecu_reset(client)
        except udsoncan.exceptions.NegativeResponseException as e:
            print(f"ECU rejected credential programming or reset: {e}")
            return

        # print("stop here")

        try:
            udsc.enter_extended_diagnostic_session(client)
        except RuntimeError as e:
            print(f"{e}")
            return

        try:
            udsc.verify_integrity(client)
        except udsoncan.exceptions.NegativeResponseException as e:
            print(f"ECU certificate verification failed: {e}")
            return

    print("Provisioning complete")


if __name__ == "__main__":
    flow("J7V737UBEJ6E6LNRJ")
