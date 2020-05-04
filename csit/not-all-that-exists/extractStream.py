from Crypto.Cipher import AES
from pyads import ADS

handler = ADS("lsass_enc.DMP")

if handler.has_streams(): #Prints out list of streams
    for stream in handler:
        print(stream)


keyIV = handler.get_stream_content("encryption_params") #Name of stream is encryption_params

f = open("encryption_params", "wb")
f.write(keyIV)
f.close()
