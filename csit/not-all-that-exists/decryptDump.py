from Crypto.Cipher import AES

f = open("encryption_params", "rb")
keyIV = f.read()


key = keyIV[:16]
IV = keyIV[16:]

lsass_enc = open("lsass_enc.DMP", "rb")
encryptedContent = lsass_enc.read()
lsass_enc.close()

cipher = AES.new(key, AES.MODE_CBC, IV)
decrypted = cipher.decrypt(encryptedContent)

f = open("lsass_enc_Decrypted.DMP", "wb")
f.write(decrypted)
f.close()

print("Done!")
