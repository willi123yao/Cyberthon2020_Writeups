# Caged Up

### Web Services // 700 Points // 32 Solves

## Description

Having accessed the database, the attacker modified the promotion banner for a product sold on ShoppingBaba, preventing the promo code from being revealed! The promo code can be found on the website http://p7ju6oidw6ayykt9zeglwyxired60yct.ctf.sg:8181 Can you find out what was the promo code?
NOTE: You do not have to compromise/pen-test the webserver

## Solution

Opening up DevTools, we are greeted with a console message from [Phaser](https://phaser.io/):

![Image of DevTools with message from Phaser](https://raw.githubusercontent.com/willi123yao/Cyberthon2020_Writeups/master/web_services/caged-up/1.png)

Phaser is a game engine and is what powers the game here. As the hint in the comment tells us:

```html
<!-- Can i ESCAPE_? How can i DESTROY() these guards around me? Can defeating a few of them open up some gaps for me to get through? -->
```

Time to look into the code. We can search in `secret.min.js` to find the name of the game variable: 

![Variable for game](https://raw.githubusercontent.com/willi123yao/Cyberthon2020_Writeups/master/web_services/caged-up/2.png)

Now, we can try looking at the keys in DevTools using `Object.keys(escape_A)` and explore from there. A method `escape_a.world.remove()` jumps out to us as it allows us to remove arbitrary sprites. The method was found from [this site](https://www.html5gamedevs.com/topic/13241-showhide-sprites-texts/).

Now, we need the sprite variable, which can be found again by exploring the keys available: `escape_A.world.children` gives us the list of sprites. We can try `escape_a.world.remove(escape_A.world.children[x])`, where `x` is any number. However, this does not work and can only remove _all_ of the characters, including the moving main character. This is because the sprites are in groups, and each child needs to be deleted separately.

![Output from console](https://raw.githubusercontent.com/willi123yao/Cyberthon2020_Writeups/master/web_services/caged-up/3.png)

Find the child with a group and a large number of children in `escape_A.world.children[x].children` (mine was 48). Now, we can delete the sprites using `escape_a.world.remove(escape_A.world.children[x].children[y])`, where y is just any number. Except

![Error while removing child](https://raw.githubusercontent.com/willi123yao/Cyberthon2020_Writeups/master/web_services/caged-up/4.png)

oops.

This is because the children are in groups, and have to be [removed by the parent](https://dustinpfister.github.io/2018/08/26/phaser-group-remove/): `escape_A.world.children[x].remove(escape_A.world.children[x].children[y])`

![Removed one sprite](https://raw.githubusercontent.com/willi123yao/Cyberthon2020_Writeups/master/web_services/caged-up/5.png)

There needs to be a hole with two neighboring missing sprites to break out of the cage because the protagonist is fat, so keep deleting away and you'll eventually break out. If you delete Mr. Protagonist, just refresh the page and try again.

![Broke out of cage](https://raw.githubusercontent.com/willi123yao/Cyberthon2020_Writeups/master/web_services/caged-up/6.png)

## Flag

```
Cyberthon{client_sided_javascript_cant_cage_me_up}
```

