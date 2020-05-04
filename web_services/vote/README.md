# Vote

### Web Services // 220 Points // 34 Solves

## Description

An opportunity for ShoppingBaba to weed out bad actors has arrived... with public voting! Vote for the unwanted to eliminate them.  

Be warned, there are others also voting ...

## Solution

There are two solutions: 1. wait for someone to solve it and get the flag with them, or 2. solve it yourself.

For solution 1, since the website is publicly available, and the results are shared ("there are others also voting")

After opening the website, we see this screen:

![Start Screen](https://cdn.discordapp.com/attachments/585742345509797890/706672512334954506/unknown.png)

The flag may have been eliminated already. After the next cycle begins, we must vote everything else (other than the flag) out, by spamming `curl` commands:

```
curl 'http://p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg:3707/' --data 'character=X'
```

multiple times, replacing X with anything from 1 to 3. If the flag still gets eliminated, you're not spamming enough. I recommend the up-arrow+enter cheatcode.

It seems like the flag is automatically removed after a set period, if insufficient votes for other characters are sent, or if there is a tie (don't send requests for multiple characters at the same time).

Repeat this to eliminate all the characters until only the flag is left:

![Screen when only the flag remains](https://cdn.discordapp.com/attachments/703593641377267764/706007177042722877/unknown.png)

Then, click on the flag to reveal the actual flag:

![Flag](https://cdn.discordapp.com/attachments/703593641377267764/706007913520562276/unknown.png)

## Flag

```
Cyberthon{next-time-buy-stuff-votes-Sm3hAOri}
```
