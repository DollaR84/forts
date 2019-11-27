# forts
Forts game on pygame

A somewhat simplified version of the board game: Sea Battle - Forts.
 
The strategic goal of the game is to capture all forts.
The player and his opponent have the following objects:
  fort - 2;
  mine - 4;
  torpedo - 6;
The following ships are also available, located to reduce power:
  battleship - 2;
  cruiser - 5;
  destroyer - 6;
  guard - 6;
  torpedo boat - 6;
  minesweeper - 6;
  submarine - 2;
Ships can be combined into squadrons, but there are limitations:
  only identical ships can be combined into a squadron;
  no more than three ships can be combined into one squadron;
Forts are motionless, only ships can capture them.
Torpedoes destroy any ship.
Mines destroy any ship except a minesweeper.
Minesweepers destroy enemy mines.
Submarines destroy only the battleship.
All other ships, depending on the strength of the ship.
If a squadron enters the battle, then the force of the squadron is taken as the sum of the forces of its ships.
If the strength of the squadrons is equal, then the squadron with fewer ships is destroyed.
If equal ships collide in battle, both are destroyed.
All moving objects can move one cell, and only a torpedo boat can move 2 cells.
