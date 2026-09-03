# import logging

import udsoncan
from udsoncan.client import Client

import cloud_client
import uds_client as udsc
from transport import clientaddress, build_isotp_stack

# logging.basicConfig(level=logging.INFO)
# log = logging.getLogger("provision")

# The ECU answered but refused the request.
ECU_REJECTED = (udsoncan.exceptions.NegativeResponseException,)

# enter_extended_diagnostic_session is wrapped in @retry_until_success(), which
# raises RuntimeError once it has used up its attempts.
ECU_UNREACHABLE = (RuntimeError,)


class StepFailed(Exception):
    """Signals that a step already reported its own failure and flow() should stop."""


def _step(description, fn, errors=ECU_REJECTED):
    try:
        return fn()
    except errors as e:
        print(f"{description} failed: {e}")
        raise StepFailed(description) from e


def flow(vin):
    isoconn, udsconfig = build_isotp_stack(clientaddress)

    with Client(isoconn, config=udsconfig) as client:
        try:
            _step("enter extended session",
                  lambda: udsc.enter_extended_diagnostic_session(client),
                  errors=ECU_UNREACHABLE)

            _step("write VIN", lambda: udsc.write_did(client, 'vin', vin))
            csr = _step("read CSR", lambda: udsc.read_did(client, 'csr'))

            # to be implemented
            creds = cloud_client.get_cert(csr)

            _step("write device ID", lambda: udsc.write_did(client, 'device_id', creds['device_id']))
            _step("write VIN alias", lambda: udsc.write_did(client, 'vin_alias', creds['vin_alias']))
            _step("write device certificate", lambda: udsc.write_did(client, 'device_cert', creds['device_cert']))
            _step("reset ECU", lambda: udsc.ecu_reset(client))

            _step("reconnect after reset",
                  lambda: udsc.enter_extended_diagnostic_session(client),
                  errors=ECU_UNREACHABLE)

            _step("verify certificate integrity", lambda: udsc.verify_integrity(client))
        except StepFailed:
            return

    print("Provisioning complete")


if __name__ == "__main__":
    flow("J7V737UBEJ6E6LNRJ")
