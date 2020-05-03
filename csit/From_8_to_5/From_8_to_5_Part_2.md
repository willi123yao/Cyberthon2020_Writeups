## From 8 to 5 Part 2

As a clue in the challenge title "From 8 to 5", this is a Base32 encoding challenge. What Base32 encoding does is to encode every character of **8** bits to **5** bits. Hence, depending on the position of your plaintext **"Cyberthon{"**, you will get 5 possible outcomes. (*because gcd(5,8) = 5!*) 

```
b32.base32_encode('Cyberthon{') = rlkdcioa0pzbujsj
b32.base32_encode('*Cyberthon{') = yt5qaxsy0tfb3jj0vn999999
b32.base32_encode('**Cyberthon{') = yrwcbuo1nwierf7vlim39999
b32.base32_encode('***Cyberthon{') = yrw1z3jintaqcm7rlmqed999
b32.base32_encode('****Cyberthon{') = yrw1zha7vypbhkszl5qdkux9
```

After removing the padding character '9' and Base32 characters that are encoding the padding and '*',  you will be left with these 5 strings.

```
rlkdcioa0pzbujsj
5qaxsy0tfb3jj0v
buo1nwierf7vlim
3jintaqcm7rlmqe
7vypbhkszl5qdku
```

*Interesting note for you: Sometimes encoded strings might have corrupted headers, so you might not know where to start with. So if you Base64 decode (most common encoding method) the string, you might get gibberish.. however, decoding after accounting for its positions might give you the correct plaintext.*

Refer to `how_to_use_SNORT.txt` to learn how to write and configure snort rules. Add the following to `/etc/snort/rules/local.rules`. For this Cyberthon challenge, you can replace the IP and ports for both source and destination as it is already configured by you running the 'malware'.

```
# generate an alert on your terminal then logs the packet
alert tcp any any -> any any (msg:"Cyberthon flag!"; content:"rlkdcioa0pzbujsj"; sid:1000001;)
alert tcp any any -> any any (msg:"Cyberthon flag!"; content:"5qaxsy0tfb3jj0v"; sid:1000002;)
alert tcp any any -> any any (msg:"Cyberthon flag!"; content:"buo1nwierf7vlim"; sid:1000003;)
alert tcp any any -> any any (msg:"Cyberthon flag!"; content:"3jintaqcm7rlmqe"; sid:1000004;)
alert tcp any any -> any any (msg:"Cyberthon flag!"; content:"7vypbhkszl5qdku"; sid:1000005;)

# log the alerted packet dump in /var/log/snort
log tcp any any -> any any (msg:"Cyberthon flag!"; content:"rlkdcioa0pzbujsj"; sid:1000006;)
log tcp any any -> any any (msg:"Cyberthon flag!"; content:"5qaxsy0tfb3jj0v"; sid:1000007;)
log tcp any any -> any any (msg:"Cyberthon flag!"; content:"buo1nwierf7vlim"; sid:1000008;)
log tcp any any -> any any (msg:"Cyberthon flag!"; content:"3jintaqcm7rlmqe"; sid:1000009;)
log tcp any any -> any any (msg:"Cyberthon flag!"; content:"7vypbhkszl5qdku"; sid:10000010;)
```

Start the SNORT sniffing. Once an alert comes up, extract the data from the packet found in the packet dump in `/var/log/snort`. 

```
ty17znp3bzma6whsrwtck3hlrzmyboa1ny5b1ohsnwienioaophqbioaywrecjjblydbhkijc5bzhzfsry7zh0a7vypbhkszl5qdkuj7lwa7zkjylia1fot1ymaqrxiv053qbkjqn3p1xrpvnwfbbojsl53drjjqcrmduk1g0pzdfitfb6k76n5lbcjs6n5jvzma6w1ttw1szntwe6k7bliibxj76999
```

Base32 decode it with your key and the flag is found within!

```
ID:205; USERNAME:S.BaBa-Server\User-Profiles; MESSAGE:Cyberthon{cmd:send--"/etc/passwd","/etc/shadow";op_time:0800-1700;}; TIME:1588379660
```

Easter egg: We come full circle as the malware command's op_time is also 'From 8 to 5'. :)

