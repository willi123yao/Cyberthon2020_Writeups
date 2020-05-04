# What You See is Not all That Exists

### CSIT // 2100 Points // 0 Solves

_This challenge was solved after Cyberthon ended._

## Description

Attackers have taken control of a Win 10 equivalent server and denied  access to it by changing the password of the "sb_admin" account. 

All you have is a LSASS memory dump of the server in NTFS format but  unfortunately, it is encrypted! It is known that the attackers have a  greater predisposition towards 7-char passwords that are composed of  uppercase and digit characters. Can you find the new password to recover control of the server? Enter the flag as Cyberthon{<password>}.

## Solution

### Decrypting the dump

The challenge name hints at a way of hiding files in others. In this case, it made use of [NTFS Alternate Data Streams](https://docs.microsoft.com/en-us/archive/blogs/askcore/alternate-data-streams-in-ntfs). We can check this by using PowerShell (or cmd):

```
> Get-Item lsass_enc.DMP -stream *

PSPath        : Microsoft.PowerShell.Core\FileSystem::C:\lsass_enc.DMP::$DATA
PSParentPath  : Microsoft.PowerShell.Core\FileSystem::C:\
PSChildName   : lsass_enc.DMP::$DATA
PSDrive       : C
PSProvider    : Microsoft.PowerShell.Core\FileSystem
PSIsContainer : False
FileName      : C:\lsass_enc.DMP
Stream        : :$DATA
Length        : 36787808

PSPath        : Microsoft.PowerShell.Core\FileSystem::C:\lsass_enc.DMP:encryption_params
PSParentPath  : Microsoft.PowerShell.Core\FileSystem::C:\
PSChildName   : lsass_enc.DMP:encryption_params
PSDrive       : C
PSProvider    : Microsoft.PowerShell.Core\FileSystem
PSIsContainer : False
FileName      : C:\lsass_enc.DMP
Stream        : encryption_params
Length        : 32
```

```
> Get-Content -Path "C:\lsass_enc.DMP" -stream encryption_params
yŒù'ÕH˜ZšVqXw•‘ZœOÙÓ
```

The name `encryption_params` suggests that this stream contains information about the encryption (i.e the **key**)

Obviously, we can't use the string given to decrypt the file. However, we can take note of a few features that lead us to the cipher used (*other than getting hint #2*):

* It's probably AES, because AES is holy
* The `encryption_params` ADS is 32 bytes long. Subtracting a 16 byte Initialization Vector (IV) from this, we know that this is a 16 byte key, which corresponds to AES-128
* The ciphertext length is a multiple of 16, making it likely that this is CBC

Hence, we can assume that this is AES-CBC-128. Now, it's time to write code to decrypt this:

```javascript
const aesjs = require('aes-js');
// Package to read ADS
const ads = require('fs-ads');
const fs = require('fs');

const params = ads.getSync('lsass_enc.DMP', 'encryption_params', {encoding: 'hex'});
let key = [];
let iv = [];
// This assumes that the string given follows the format KEY then IV
// IV then KEY does not create valid output
for (let i = 0; i < 16; i++) key.push(parseInt(params.substr(i * 2, 2), 16));
for (let i = 16; i < 32; i++) iv.push(parseInt(params.substr(i * 2, 2), 16));

let aesCbc = new aesjs.ModeOfOperation.cbc(key, iv);
let decryptedBytes = aesCbc.decrypt(fs.readFileSync('lsass_enc.DMP'));

fs.writeFileSync('out', decryptedBytes);
```

<u>**Note:**</u> Powershell commands seem to output the contents of the stream incorrectly. Use JS like above or a python module such as [PyADS](https://github.com/RobinDavid/pyADS) to extract the content instead. [See [extractStream.py](extractStream.py) and [decryptDump.py](decryptDump.py) for Python. Split into 2 parts as extractStream needs to be ran on Windows]

This creates a file `out` that _should_ be the LSASS dump. We can verify this by using mimikats (disable your antivirus) by following [this guide](https://medium.com/@markmotig/some-ways-to-dump-lsass-exe-c4a75fdc49bf#2854):

```
> .\mimikatz.exe "sekurlsa::minidump out"

  .#####.   mimikatz 2.2.0 (x64) #18362 Jan  1 1970 00:00:00
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

mimikatz(commandline) # sekurlsa::minidump out
Switch to MINIDUMP : 'out'

mimikatz # sekurlsa::LogonPasswords
Opening : 'out' file for minidump...

...

Authentication Id : 0 ; 209894 (00000000:000333e6)
Session           : Interactive from 1
User Name         : sb_admin
Domain            : WIN-07QUV32RIAR
Logon Server      : WIN-07QUV32RIAR
Logon Time        : 2/20/2020 10:02:19
SID               : S-1-5-21-1172315603-1254066301-3879487369-1000
        msv :
         [00000003] Primary
         * Username : sb_admin
         * Domain   : WIN-07QUV32RIAR
         * NTLM     : b381519f1f1f330c4301c4be59ac0d62
         * SHA1     : c55bfa8fa09760919fdeb0c2f5bb5a022c926903
        tspkg :
        wdigest :
         * Username : sb_admin
         * Domain   : WIN-07QUV32RIAR
         * Password : (null)
        kerberos :
         * Username : sb_admin
         * Domain   : WIN-07QUV32RIAR
         * Password : (null)
        ssp :
        credman :

...

Authentication Id : 0 ; 999 (00000000:000003e7)
Session           : UndefinedLogonType from 0
User Name         : WIN-07QUV32RIAR$
Domain            : WORKGROUP
Logon Server      : (null)
Logon Time        : 2/20/2020 10:01:46
SID               : S-1-5-18
        msv :
        tspkg :
        wdigest :
         * Username : WIN-07QUV32RIAR$
         * Domain   : WORKGROUP
         * Password : (null)
        kerberos :
         * Username : win-07quv32riar$
         * Domain   : WORKGROUP
         * Password : (null)
        ssp :
        credman :
```

*Output truncated*

The NTLM hash for the user is `b381519f1f1f330c4301c4be59ac0d62`. For some reason, there were a lot of `(null)` entries like the last one.

*Note:* This is the output given if the decryption failed:

```
> .\mimikatz.exe "sekurlsa::minidump out"

  .#####.   mimikatz 2.2.0 (x64) #18362 Jan  1 1970 00:00:00
 .## ^ ##.  "A La Vie, A L'Amour" - (oe.eo)
 ## / \ ##  /*** Benjamin DELPY `gentilkiwi` ( benjamin@gentilkiwi.com )
 ## \ / ##       > http://blog.gentilkiwi.com/mimikatz
 '## v ##'       Vincent LE TOUX             ( vincent.letoux@gmail.com )
  '#####'        > http://pingcastle.com / http://mysmartlogon.com   ***/

mimikatz(commandline) # sekurlsa::minidump out
Switch to MINIDUMP : 'out_swapped'

mimikatz # sekurlsa::LogonPasswords
Opening : 'out_swapped' file for minidump...
ERROR kuhl_m_sekurlsa_acquireLSA ; Handle on memory (0x00000002)
```

### Getting the password

Because my computer is quite slow (this seems unnecessary in retrospect), I decided to use [Colab](https://colab.research.google.com/drive/1UefhU0VRWHO_YxkFqZ5g-bJiHFX7XC2A) to do the hash cracking by following [this guide](https://gist.github.com/koenrh/801766782fe65b279b436576d935d5d3) _(kinda)_.

To start the process, ensure that a GPU session is selected. Then, download and extract the latest version of hashcat:

```
!wget https://github.com/hashcat/hashcat/releases/download/v5.1.0/hashcat-5.1.0.7z
!7zr x hashcat-5.1.0.7z
!chmod a+x hashcat-5.1.0/hashcat64.bin
```

Set up the GPU (apparently this speeds up something, according to the guide). This was done using a P100 instance:

```
# Speeds something up or something according to the guide
# This was run using a P100 instance
!nvidia-smi --persistence-mode=ENABLED
!nvidia-smi -q -i 0 -d SUPPORTED_CLOCKS
==============NVSMI LOG==============
Timestamp                           : Thu Jan  1 00:00:00 1970
Driver Version                      : 418.67
CUDA Version                        : 10.1
Attached GPUs                       : 1
GPU 00000000:00:04.0
    Supported Clocks
        Memory                      : 715 MHz
            Graphics                : 1328 MHz
            Graphics                : 1316 MHz
...

!nvidia-smi --applications-clocks=715,1328
```

And finally crack the hash using a [mask](https://hashcat.net/wiki/doku.php?id=mask_attack):

```
!./hashcat-5.1.0/hashcat64.bin -m 1000 -a 3 -o passwd b381519f1f1f330c4301c4be59ac0d62 -1 ?u?d ?1?1?1?1?1?1?1

hashcat (v5.1.0) starting...

nvmlDeviceGetFanSpeed(): Not Supported

OpenCL Platform #1: NVIDIA Corporation
======================================
* Device #1: Tesla P100-PCIE-16GB, 4070/16280 MB allocatable, 56MCU

Hashes: 1 digests; 1 unique digests, 1 unique salts
Bitmaps: 16 bits, 65536 entries, 0x0000ffff mask, 262144 bytes, 5/13 rotates

Applicable optimizers:
* Zero-Byte
* Early-Skip
* Not-Salted
* Not-Iterated
* Single-Hash
* Single-Salt
* Brute-Force
* Raw-Hash

Minimum password length supported by kernel: 0
Maximum password length supported by kernel: 256

ATTENTION! Pure (unoptimized) OpenCL kernels selected.
This enables cracking passwords and salts > length 32 but for the price of drastically reduced performance.
If you want to switch to optimized OpenCL kernels, append -O to your commandline.

Watchdog: Temperature abort trigger set to 90c

The wordlist or mask that you are using is too small.
This means that hashcat cannot use the full parallel power of your device(s).
Unless you supply more work, your cracking speed will drop.
For tips on supplying more work, see: https://hashcat.net/faq/morework

Approaching final keyspace - workload adjusted.

                                                 
Session..........: hashcat
Status...........: Cracked
Hash.Type........: NTLM
Hash.Target......: b381519f1f1f330c4301c4be59ac0d62
Time.Started.....: Sun May  3 03:43:04 2020 (4 secs)
Time.Estimated...: Sun May  3 03:43:08 2020 (0 secs)
Guess.Mask.......: ?1?1?1?1?1?1?1 [7]
Guess.Charset....: -1 ?u?d, -2 Undefined, -3 Undefined, -4 Undefined 
Guess.Queue......: 1/1 (100.00%)
Speed.#1.........: 10605.2 MH/s (4.64ms) @ Accel:64 Loops:32 Thr:1024 Vec:1
Recovered........: 1/1 (100.00%) Digests, 1/1 (100.00%) Salts
Progress.........: 44073123840/78364164096 (56.24%)
Rejected.........: 0/44073123840 (0.00%)
Restore.Point....: 0/1679616 (0.00%)
Restore.Sub.#1...: Salt:0 Amplifier:26208-26240 Iteration:0-32
Candidates.#1....: 17T4567 -> YS2QFZV
Hardware.Mon.#1..: Temp: 42c Util: 93% Core:1328MHz Mem: 715MHz Bus:16

!cat passwd
b381519f1f1f330c4301c4be59ac0d62:CY20BER
```

As seen here, the hash was "too easy" for the GPU, and this was quite overkill. In total, this script took 10 seconds to run.

## Flag

```
Cyberthon{CY20BER}
```
