# Game_Of_Life

Python Game Of Life 
project implementation with pygame

Description:
Implementation of the game "Game of Life" in pygame. The game supports buttons:
- START / STOP (simulation - 500ms)
- SAVE / LOAD (Game state)
- NEXT (Next iteration)

Video:
https://youtu.be/RabA_BBtGjg

Design patterns:
- Abstract Factory - used to create new instances of buttons like: START / STOP / SAVE / LOAD / NEXT
- Observer - used to update the game view only in case of game_state change
