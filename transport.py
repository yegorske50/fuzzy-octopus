import config
from config import DIDS

import isotp
import udsoncan
import udsoncan.configs
from udsoncan.client import Client
from udsoncan.connections import IsoTPSocketConnection

class RawUTFCodec(udsoncan.DidCodec):
    def encode(self, val):
        return val.encode("utf-8")
    def decode(self, payload):
        return payload.decode("utf-8")
    def __len__(self):
        raise udsoncan.DidCodec.ReadAllRemainingData

clientaddress = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=config.TESTER_TX_ID, rxid=config.ECU_TX_ID)
# addr = isotp.Address(addressing_mode=isotp.AddressingMode.Normal_11bits, txid=config.TESTER_TX_ID, rxid=config.ECU_TX_ID, target_address=None, source_address=None, physical_id=None, functional_id=None, address_extension=None, rx_only=False, tx_only=False)

ecuaddress = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=config.ECU_TX_ID, rxid=config.TESTER_TX_ID)


tpsock = isotp.socket()
# tpsock.set_fc_opts(bs=8, stmin=0)
# tpsock.set_opts(optflag=None, frame_txtime=None, ext_address=None, txpad=None, rxpad=None, rx_ext_address=None, tx_stmin=None)
# tpsock.set_ll_opts(mtu=None, tx_dl=None, tx_flags=None)

isoconn = IsoTPSocketConnection(config.CAN_INTERFACE, clientaddress, tpsock=tpsock)

udsconfig = dict(udsoncan.configs.default_client_config)
# print(udsconfig)

# {
#   "exception_on_negative_response": true,
#   "exception_on_invalid_response": true,
#   "exception_on_unexpected_response": true,
#   "security_algo": null,
#   "security_algo_params": null,
#   "tolerate_zero_padding": true,
#   "ignore_all_zero_dtc": true,
#   "dtc_snapshot_did_size": 2,
#   "server_address_format": null,
#   "server_memorysize_format": null,
#   "data_identifiers": {},
#   "input_output": {},
#   "request_timeout": 5,
#   "p2_timeout": 1,
#   "p2_star_timeout": 5,
#   "standard_version": 2020,
#   "use_server_timing": true,
#   "extended_data_size": null,
#   "nrc78_callback": null
# }


udsconfig['data_identifiers'] = {DIDS['vin']: RawUTFCodec()}
udsconfig['p2_timeout'] = 0.5 
udsconfig['p2_star_timeout'] = 5.0 
udsconfig['use_server_timing'] = False 
