#  Text is the key

### Network Security // 200 Points // 0 Solves

*This challenge was solved after Cyberthon ended.*

## Part 1

The first part of this challenge was done by matching each number to a character in the string:

```python
original = 'ShoppingBaba is a e-commerce platform headquartered under the ShoppingBaba Group,  which was founded in 2009 by Baba Sho. ShoppingBaba first launched in Babaland in 2016,  and since expanded its reach globally. Due to the mobile and social element built within the concept,  ShoppingBaba was described as one of the "4 disruptive ecommerce startups we saw in 2017" by Global Tech.(Updated on 03.05.2018)'

chs = [33, 2, 19, 18, 136, 125, 209, 318, 319, 252, 181, 298, 120, 399, 391, 208, 359, 391, 168, 208, 34, 11, 231, 276, 94, 294, 251, 209, 318, 319, 209, 109, 104, 168, 107, 272, 269, 236, 350, 175, 83, 233, 137, 186, 272, 14, 15, 209, 394, 399, 381, 165, 113, 394, 112, 107, 391, 359, 394, 381, 391, 360, 315, 359]

st = ""
for ch in chs:
	print ch
	st += original[ch-1]

print(st)
```

```
the ip is ed.83.136.fb port is b269 password is 58d2a5B9315d3741
```

Kudos you did this by hand. Obviously, the IP and port are not valid and need a further step of decoding.

## Part 2

This part was done after Cyberthon ended. The answer was basically provided by CSIT_junhao:

> For text is the key, after you get the encoded IP + port, you actually need to decode it 2 times to get to the correct value.  
> e.g.  port = `b269` (base 16) ➝ `45673` (base 10)  
> `45673` (base 8) ➝ `19387` (base 10)

During the competition, I decoded it from hex to decimal, but did not take the extra step of decoding from oct. This yields an IP beginning with `237`, which is invalid.

The Windows Calculator (in the "Programmer" mode) turns out to be a surprisingly handy tool for this (CyberChef thinks that the hex values are in bytes, which is not true):

* The IP was decoded after being spliced by colons: `159.89.200.169`
* The port was provided (decodes the same way): `19387`

* The password decodes to `117 110 104 105 100 101`. Conveniently, the spaces added correspond to ASCII. Using CyberChef, we can decode this to be `unhide`.

Now, we can connect to the website and we get a prompt for the password. However, the password `unhide` does not work here. Apparently, the conversion to ASCII was a decoy of sorts and `117110104105100101` is the correct password.

## Flag

```
Cyberthon{y0ufoundmy1p} 
```
