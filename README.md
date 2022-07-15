# Galaxy Traveller
This is a small game I built with the pygame library for a science festival at my school (Hội vui Khoa học Tự nhiên Chuyên Ngoại Ngữ 2021)
In this game, you control a spaceship. Your objective is to collect as many coins and kill as many enemy spaceships as possible. _The score is measured  by `coins + kills*2`_  
There are two types of enemies:
+ Type 1: the smaller one, capable of shooting in 4 directions (like a plus sign) if you are within its shooting range
+ Type 2: the bigger one, capable of passing through walls, causing an explosion upon close contact
There are also boosts to help you destroy your enemies easier:
+ Ricochet bullets
+ Multishot (3 bullets at once)
+ Super speed (x2 current speed)
I have finished this game a long time ago, but I think might update this game again in my spare time.
Upcoming features: 
+ Settings menu: allow you to control the walls, and shooting range of enemies that belong to type 1.
In fact you can change in settings.json. But I want to make a menu
+ Wormholes: 2 wormholes spawn randomly. You can travel through them
+ Healthbar maybe ?

In this patch I reformat some part of the code.

Anyways here is an screenshot of the game:
![Screenshot](./demo/screenshot1.png)

## Running the project
Dependencies: `pygame` (`cx_freeze` if you want to build the game)

Run `menu.py` to start the game

If you intend to create an executable, make the following change to `menu.py`
Change the import line:
`import pygame, sys, os, engine #engine_exec`
to `import pygame, sys, os, engine_exec`
and thus, the run game line:
```
def new_game():
    #engine_exec.game()
    engine.game()
```    
to 
```
def new_game():
    engine_exec.game()
```

Run `python setup.py build` and you will get an executable in `build` folder, just like the executable I included.
