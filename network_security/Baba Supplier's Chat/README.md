# Baba Supplier's Chat

**ShoppingBaba uses a chat server to interact with their suppliers.**

**Their suppliers connects to this chat server by using a client python script. Upon connecting, the server usually will provide the supplier with a random username with password for login purposes.**

**However, suppliers now complain that the connection ends too quickly and they can no longer login!**

**Investigate the client script and connect to p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg:21011 to get to the bottom of this!**



We are given a python2 file `client.py`.

```python
import socket
import sys

# Create a TCP/IP socket
sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Connect the socket to the port on the server given by the caller
if len(sys.argv) < 3:
    print 'usage: client.py [server_address] [server_port]'
    sys.exit(1)  # abort because of error
server_port = int(sys.argv[2])
server_address = (sys.argv[1], server_port)
print >>sys.stderr, 'connecting to %s port %s' % server_address
try:
    sock.connect(server_address)
except socket.error, (value, message):
    print 'socket.error - ' + message + ' addr: ' , server_address


try:    
    #Standard login
    data = sock.recv(1024)
    print >>sys.stderr, 'received "%s"' % data
    print 'sending "%s" ' % "shake_baba"
    sock.sendall("shake_baba")
    data = sock.recv(1024)
    print >>sys.stderr, 'received "%s"' % data

    # Reply hash of the message send to login
    print 'sending hashed "%s" ' % str(data)
    sock.sendall(str(hash(data)))

    data = sock.recv(1024)
    print >>sys.stderr, 'received "%s"' % data

    # Get login credentials
    print 'sending hashed "%s" ' % str(data)
    sock.sendall("Hello!")

    data = sock.recv(1024)
    print >>sys.stderr, 'received "%s"' % data
    
    

except socket.error, (value,message): 
    count = 0;
    print 'socket.error - ' + message + ' addr: ' , server_address 

finally:
    sock.close()

```

When we first run this file, we get the following output:

```bash
python2 client.py p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg 21011
connecting to p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg port 21011
received "Welcome to ShoppingBaba Supplier's Chat Server!"
sending "shake_baba"
received "effect"
sending hashed "effect"
received "onlinetools"
sending hashed "onlinetools"
received ""
```

Hmm... it seems to end after a few sends. Looking back at the code, we realise that the last `sock.sendall` simply sends a "Hello" instead of the hashed data. I first rectified this, but it then simply sent and received another word. Maybe we need to *spam* the server until a flag somehow pops out!

With that in mind, I wrote the following python code:

```python
while True:
    data = sock.recv(1024)
    print >>sys.stderr, 'received "%s"' % data

    if (data != b""):
        print 'sending hashed "%s" ' % str(data)
        sock.sendall(str(hash(data)))
    else:
        break
```

Sure enough, after sometime:

```bash
.....
sending hashed "class"
received "fully"
sending hashed "fully"
received "leave"
sending hashed "leave"
received "sing"
sending hashed "sing"
received "Cyberthon{chat_pwned}"
sending hashed "Cyberthon{chat_pwned}"
received ""
received ""
```

Hence, the flag is:

```bash
Cyberthon{chat_pwned}
```

