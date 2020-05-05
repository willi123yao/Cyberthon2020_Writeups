import json
from Crypto.Cipher import AES
content = json.load(open("Packets.json", "r"))

httpPacketData = []


#Filter out all http packets with data
for x in content:
    layers = x["_source"]["layers"]
    if "http" in layers:
        if "data" in layers:
            data = layers["data"]["data.data"]
            data = data.split(":")
            data = "".join(data)
            byteData = bytes.fromhex(data)
            httpPacketData.append(byteData)

currentPacketNo = 1041 #starting packet number in plaintext
packet = httpPacketData[currentPacketNo-1]

for x in range(0, 2020, 1):

    key = packet[packet.find(b"Key:")+4:packet.find(b"Key:")+36].decode()
    IV = packet[packet.find(b"IV:")+3:packet.find(b"IV:")+35].decode()
    currentPacketNo = int(packet[packet.find(b"Next-ID:")+8:packet.find(b"Next-ID:")+14].decode()) #set to next packet no.

    packet = httpPacketData[currentPacketNo-1]

    cipher = AES.new(bytes.fromhex(key), AES.MODE_CBC, bytes.fromhex(IV))
    packet = cipher.decrypt(packet)

    if b"Cyberthon{" in packet:
        print(packet)
        break
            
        
            
        