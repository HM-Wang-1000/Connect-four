# Overview

This Connect-four game bases on python and supports local 2-player and human vs computer with three difficulty levels. Level 3 uses Minimax with adjustable depth. Note that α-β pruning is ***not*** used in the code, so please don't set a great depth, or the code might be very slow.

# How To Play

(1)This game is only based on python. No extra libraries required. Simply open the .py file and follow the prompt, first choose the mode(pvp or pve), then the sequence and finally the difficulty(these two choices are only available when the first choice is "2", i.e. pve mode). Then just follow the prompts included in the file and have fun!

# What computers do in different difficulties

(1)For the first difficulty, it will simply choose a random column in all available choices. It will ***not*** care if this step will make you win directly, or if there is another better choice that it can win directly.

(2)For the second difficulty, it will follow some basic rules I set, including: 1. If there is a choice that directly leads to winning, it will take it. 2. If there is a choice that can directly leads to failure, it will 
not take it. In other words, it will prevent helping you to win. 3. If neither of 1 and 2 is happening, it will take choices randomly with a weight. Generally, the weight in the middle columns are greater, and the 
weight of columns with less height are greater.

(3)For the last difficulty, it uses Minimax. It will evaluate a score of the current board, and what will the change in the score be after taking an action on a column. It will try to maximize its score to win.

# Some other details

(1)There are sometimes comments and strings between codes. If they are in triple quetes, then it is likely a test line when I'm amending the program.

(2)This is my first project uploaded to online platform, so sorry for possible unconscious mistakes. If there are any problem, please do not hesitate to contact me through email. My email address is henry_wang2007@163.com.

# Acknowledgements

Classic Connect Four AI heuristics and Minimax inspired this implementation.


