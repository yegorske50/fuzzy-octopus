import isotp

CAN_INTERFACE = "vcan0"
TESTER_TX_ID = 0x7E0 
ECU_TX_ID = 0x7E8
DID = 0xF190
DID_VALUE = b"LEARNUDS"

address = isotp.Address(isotp.AddressingMode.Normal_11bits, txid=ECU_TX_ID, rxid=TESTER_TX_ID)

tpsock = isotp.socket()
tpsock.bind(CAN_INTERFACE, address)

print(f"ECU simulator up on {CAN_INTERFACE}")

while True:
    request = tpsock.recv()

    if request[:3] == bytes([0x22, DID >> 8, DID & 0xFF]):

        response = bytes([0x62, DID >> 8, DID & 0xFF]) + DID_VALUE
        tpsock.send(response)
        print(f"-> ReadDataByIdentifier replied {DID_VALUE}")