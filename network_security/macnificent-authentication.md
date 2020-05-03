# Macnificent Authentication

### Network Security // 665 Points // 0 Solves

## Description

The IT security manager decided that it would be "ingenious" to use products sold by this company for authentication. Employees connect to the server to login via the below method. Break the authentication and get the flag!

`nc p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg 17171`

## Solution

Connecting to the server returns the following:

```
$ nc p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg 17171
00000000:00011110:10110101
Input? : No response... Goodbye!
```

Given that this challenge is called "MAC"nificent Authentication and the other hints available, we can determine that the 3 bytes given are part of the MAC address of something. There is an automatic timeout after 5 seconds (no response), we a script must be used to speed up the decoding process:

```python
from pwn import *
r = remote('p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg', 17171)
prefix = r.readline()
mac = str(hex(int(prefix[0:8], 2)))[2:].zfill(2) + \
      str(hex(int(prefix[9:17], 2)))[2:].zfill(2) + \
      str(hex(int(prefix[18:26], 2)))[2:].zfill(2)
r.sendline(oui[mac.upper()])
print r.readline()
```

The scary looking line for the variable `mac` does the following:

1. Get an 8-byte substring from the binary given (i.e. 1 byte)
2. Convert it into an integer using `int()`, then convert it into a hex string
3. Substring the hex string for the part after the second character, since the string begins with `0x`
4. Use `zfill(2)` to add leading zeros (`0` becomes `00`, for example)

### Confusion Ensues

[Skip to the actual solution](#the-actual-solution)

This creates 3 bytes of a MAC address, but the full MAC address if 6 bytes long. Because the question hinted at the manufacturer, I'd initially assumed that the answer was supposed to be a "spoofed" MAC address that looks like it was from the manufacturer:

```
01:23:45:AB:CD:EF
  OUI   | IDENTIFIER
```

The OUI is the part of the MAC address that identifies the manufacturer. Since only 3 bytes were provided, I tried hardcoding a random value for the identifier. Any value should work (by this theory) for the identifier, since only the OUI should matter. This did not work.

Another theory was that the OUI was fixed in place. The challenge description puts "ingenious" in quotes, so I tried prepending the OUI of each company that had the substring "ingeni-" (most of these companies were just German "ingenieur" firms). This did not work either.

In a fit of desperation, I tried just repeating the MAC address given twice, to (quite obviously) no avail.

### The Actual Solution

After the competition ended, I asked the organizers for help on this challenge. It turns out that the solution is not a MAC address: rather, it should be the name of the manufacturer. To get the manufacturer name automatically, [a CSV file from IEEE that has a list of all the manufacturers and their assigned OUIs can be found](https://standards-oui.ieee.org/oui/oui.csv). By adding that to the script:

```python
from pwn import *
import csv
with open('oui.csv', mode='r') as infile:
	reader = csv.reader(infile)
    # Get the MAC address and manufacturer columns of the CSV
	oui = {col[1]:col[2] for col in reader}
	r = remote('p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg', 17171)
	prefix = r.readline()
    # The MAC address column does not have the colons in it
    # It is formatted as a capitalized string (ABCD56)
	mac = str(hex(int(prefix[0:8], 2)))[2:].zfill(2) + \
	      str(hex(int(prefix[9:17], 2)))[2:].zfill(2) + \
	      str(hex(int(prefix[18:26], 2)))[2:].zfill(2)
	r.sendline(oui[mac.upper()])
	print r.readline()
	print r.readline()
```

```
$ python mac.py
[+] Opening connection to p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg on port 17171: Done
Input? : Access granted.

Cyberthon{iH@s4llTh3MAC5}

[*] Closed connection to p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg port 17171
```

## Flag

```
Cyberthon{iH@s4llTh3MAC5}
```

## Takeaways

* I was quite fixated on generating a MAC address to send as the answer. I should have tried changing my solution after it failed so many times.
