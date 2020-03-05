# AshCode
# A new coder, interested in programming mini-games, useful tools and linguistic analyses in various front and backend languages

# QUORIDOR
# Code for a backend of a game of Quoridor (2 player version). Visualisations to come next!
# Each player starts on opposite ends of a 9x9 board and in turn they can either move 1 space up, down, left or right (not diagonally!)
# or alternatively they may play a 2x1 fence which prevents players from traversing the board. Fences cannot overlap or criss-cross
# note: if players are adjacent then the moving player may jump over the other player if there are no fences in the way
# the objective is to get to the other side of the board before the other player
# fences cannot be placed to 'trap' another player (ie. to make a win impossible for the other player)
# once a visualisation is created, my natural next step would be to simulate games to build a bot which players can play against
# built using machine learning techniques and lots of simulation data

# Players can either game.move(direction) or game.fence((coordinates, horizontal))
# where direction is 'U', 'D', 'L', 'R' or possibly 'UU', 'UL' etc where players are adjacent. See wikipedia for further explanation
# and where coordinates is the coordinates, [x,y], of the bottom-left hand corner of the 2x2 square encasing the desired location 
# of fences, and horizontal is a boolean (True, False), True meaning yes horizontal, False meaning no so vertical

# More developments to come
# Primary testing passed, possibly more bugs existing however
