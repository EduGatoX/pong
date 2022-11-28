readme.md
Project: Pong
Date: 28-11-2022

This is a simple project whose purpose is to showcase some of the
concepts and features I can manage when writing a software project.

Note: The project currently has some bugs that will be fixed shortly

Description:

1. First I created the project inside a single file (pong.py), just to make it
work to a certain extent and to get familiar with the logic of the pong
game.

2. Then, I rewrote the entire application following a MVC architecture. Here,
I introduced concepts like dataclasses, Enums, and closures, and strategy pattern
that greatly decoupled the code a made parts of the code reusable (for example, 
the render() method of the GameView class used by GameController).
I introduced a strategy pattern in the render method of the GameController class 
to be able to render different types of elements on the screen, without having 
to make the GameView class aware of what it was being rendered.

4. Finally, I created a simple event system for handling the key inputs, using
a functional approach of the observer pattern.

Following Steps:

- The project can be further improved by decoupling the GameController class of 
specific parts of both GameView and GameModel. This can be done by creating ABC's
or Protocols that can act as an interface between those parts of the application.

- In the GameModel class there are objects created inside the __init__() method.
The idea would be to create them outside using a creational design pattern, and
passed them as a parameter to the GameModel, thus following the dependency inversion
design principle.

- The project needs a config file to put the constants that are being used in the
setup of the application.