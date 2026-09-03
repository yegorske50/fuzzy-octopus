CAN_INTERFACE = "vcan0"
TESTER_TX_ID = 0x7E0 
ECU_TX_ID = 0x7E8 

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

# ECU simulator config

ECU_REBOOT_TIME = 5.0