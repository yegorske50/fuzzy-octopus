import isotp
import udsoncan
import udsoncan.configs
from udsoncan.client import Client
from udsoncan.connections import IsoTPSocketConnection

CAN_INTERFACE = "vcan0"
TESTER_TX_ID = 0x7E0 
ECU_TX_ID = 0x7E8 
DID = 0xF190 

address = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=TESTER_TX_ID, rxid=ECU_TX_ID)
# addr = isotp.Address(addressing_mode=isotp.AddressingMode.Normal_11bits, txid=TESTER_TX_ID, rxid=ECU_TX_ID, target_address=None, source_address=None, physical_id=None, functional_id=None, address_extension=None, rx_only=False, tx_only=False)

tpsock = isotp.socket()
# tpsock.set_fc_opts(bs=8, stmin=0)
# tpsock.set_opts(optflag=None, frame_txtime=None, ext_address=None, txpad=None, rxpad=None, rx_ext_address=None, tx_stmin=None)
# tpsock.set_ll_opts(mtu=None, tx_dl=None, tx_flags=None)

conn = IsoTPSocketConnection(CAN_INTERFACE, address, tpsock=tpsock)

config = dict(udsoncan.configs.default_client_config)
# print(config)

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


config['data_identifiers'] = {DID: udsoncan.AsciiCodec(8)}
config['p2_timeout'] = 0.5 
config['p2_star_timeout'] = 5.0 
config['use_server_timing'] = False 

with Client(conn, config=config) as client:
    response = client.read_data_by_identifier(DID)
    print(f"{response.service_data.values[DID]}")