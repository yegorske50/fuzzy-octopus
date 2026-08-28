CAN_INTERFACE = "vcan0"
TESTER_TX_ID = 0x7E0 
ECU_TX_ID = 0x7E8 

SESSION_DEFAULT = 0x01
SESSION_EXTENDED = 0x03

RESET_HARD = 0x01

DIDS = {
    "vin": 0xF190,
    "csr": 0xF191,
    "device_id": 0xF192,
    "vin_alias": 0xF193,
    "device_cert": 0xF194,
}

ROUTINES = {
    "verify_certificate_integrity": 0x0203,
}