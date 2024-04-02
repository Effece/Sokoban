# Sokoban
I remade Sokoban in Python using Tkinter. This was made in Summer 2021.

## How to play
You are placed on a grid with a player, boxes, crosses and walls. By moving into a box, you push it forward. You can't pull back a box or walk on it.
Your objective is to move every box on a cross which gets you to the next level.

## Multi-player mode
The only addition I made was the multi-player mode.
Many players are spawned on the grid and each move moves each player. For example, if you move to the right, every player attempts to move to the right. Those who are blocked by a wall won't move.
This brings new strategies. Two levels have the player stuck in a small space where he can't move up too much or else a box gets unmovable.

## Files and maker program
Among the files, there are the two main programs, the one containing the levels and a level maker. The level maker generates a grid on which you can add the elements as you want, then it generates a list that you can implement in the levels file.

## Levels
Many levels were found online and most if not all of them were published in a lot of different recreations so I don't have credits. A few 1-player levels and every multi-player level are my creations though.

## Graphics
Tkinter being known for its great image rendering, the textures aren't images but drawn polygons. Your computer may not enjoy your playthrough sometimes.
