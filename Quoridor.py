import numpy as np
import random


class Quoridor() :
    no_of_players = 2 #in a later version of this let's make this dynamic (4 players possible)
    #easily done by taking self.no_of_players = number of arguments, with 2 and 4 players as only valid inputs
    first_player = random.choice(["Player 1", "Player 2"]) #randomly choose who goes first
    moving_player = first_player #'moving' player from now on refers to he/she whose move it is
    if first_player[-1] == "1" :
        waiting_player = f"{first_player[:-1]}2"
    elif first_player[-1] == "2" :
        waiting_player = f"{first_player[:-1]}1" 
    #'waiting' player is he/she who is waiting for opponents move to be made
    no_of_moves = 0 #initialise with 0 moves made (as of yet)
    rules = "Rules:" #here let's have an explanation of the rules to call on
    fences_dict = dict([["Player 1", 10],["Player 2", 10]]) #a dictionary of respective remaining fences
    start_positions = dict([["Player 1", [0,4]],["Player 2", [8,4]]]) 
    players_adjacent = False #are the players adjacent (ie to the immediate L, R, U, D of each other)
    current_positions = start_positions #current_positions to be changed throughout, obviously
    #board is a 9x9 array of possible moves, 'U' representing Up etc, 1 meaning possible... etc
    #note: a level of redundancy arises here, as being able to move up from [x,y]
    #ought to be the same as being able to move down from [x,y+1]
    #as this is a small game I doubt it's worth worrying about, but consider more memory efficient options
    board = np.array([[dict([['U', 1], ['D', 1], ['L', 1],['R',1]]) for x in range(9)] for y in range(9)])
    for counter in range(9) :
        #imitates idea of encasing for the board (cannot leave the board!)
        board[8][counter]['U'] = 0
        board[0][counter]['D'] = 0
        board[counter][0]['L'] = 0
        board[counter][8]['R'] = 0

    def __init__(self, player1, player2) :
        '''initialised with two parameters: name of player 1 and name of player 2. The game begins immediately'''
        self.names_dict = dict([["Player 1", player1],["Player 2", player2]])
        print(self.rules)
        print(f"Player 1: {player1}")
        print(f"Player 2: {player2}")
        print(f"The first move is to be made by: {self.first_player}")
        self.game_in_progress = True
        #this last attribute is probably pointless, but we shall see

    def swap_axis(self, direction) :
        '''given a direction on the horizontal axis this will return vertical directions and viceversa'''
        if direction in ['U', 'D'] :
            return(['L', 'R'])
        elif direction in ['L', 'R'] :
            return(['U', 'D'])

    def opposite_direction(self, direction) :
        '''given a direction, return the direction a 180 degree turn from this'''
        if direction == 'L' :
            return('R')
        elif direction == 'R' :
            return('L')
        elif direction == 'U' :
            return('D')
        elif direction == 'D' :
            return('U')

    def position(self, player='moving') :
        '''returns the current position of the selected player: the moving player is the default'''
        if player in ['moving', 'waiting'] :
            pos = self.current_positions[getattr(self, f"{player}_player")]
            y,x = pos
            return([x,y])
        else :
            #note: this is an internal function, so cannot necessarily be misused. Perhaps this is needless
            raise Exception

    def swap_perspective(self) :
        '''updates who is the moving player and who is the waiting player (after a move is made)'''
        temp1 = self.moving_player
        temp2 = self.waiting_player
        self.moving_player = temp2
        self.waiting_player = temp1

    def check_if_adjacent(self, return_details=False) :
        '''checks if players are adjacent each other (ie directly above, below, to the left or to the right)
        if return_details == True then will return which direction the waiting_player is wrt the moving_player
        note: this updates the attribute self.players_adjacent with the appropriate value'''
        x,y = self.position()
        x_wait, y_wait = self.position('waiting')
        if y != y_wait and x != x_wait :
            self.players_adjacent = False
            info = None
        elif y == y_wait and x == x_wait + 1 :
            self.players_adjacent = True
            info = 'L'
        elif y == y_wait and x == x_wait - 1 :
            self.players_adjacent = True
            info = 'R'
        elif y == y_wait + 1 and x == x_wait :
            self.players_adjacent = True
            info = 'D'
        elif y == y_wait - 1 and x == x_wait :
            self.players_adjacent = True
            info = 'U'
        else :
            self.players_adjacent = False
            info = None
        if return_details == True :
            return(info)
        else :
            return(None)

    def print_positions(self) :
        print(f"{self.moving_player}: ({self.names_dict[self.moving_player]}) has position {self.position()}")
        print(f"{self.waiting_player}: ({self.names_dict[self.waiting_player]}) has position {self.position(player='waiting')}")

    def options(self, position = None, details = False) :
        '''returns the set of legal moves that can be made by the moving player on the current board
        if details == True then it considers adjacent pawn complications
        if position == [x,y] defined explicitly, returns possible moves for that hypothetical pawn'''
        if position == None :
            position = self.position()
        x,y = position
        options = [direction for direction, boolean in self.board[y][x].items() if boolean == 1]
        if details == False :
            #no consideration of adjacent pawns requested
            return(options)
        else :
            adjacent_check = self.check_if_adjacent(return_details=True)
            if self.players_adjacent == True :
                x_wait, y_wait = self.position('waiting')
                options_wait = [direction for direction, boolean in self.board[y_wait][x_wait].items() if boolean == 1]
                for d in options :
                    if adjacent_check == d :
                        options.remove(d)
                        if d in options_wait :
                            options.append(f"{d}{d}")
                        else :
                            for direction in self.swap_axis(d) :
                                if direction in options_wait :
                                    options.append(f'{d}{direction}')
                    else :
                        continue
                #here we found adjacent pawn complications and added extra options accordingly
                return(options)
            else :
                #here we have considered adjacent pawns and found no complications
                return(options)

    def print_options(self) :
        '''prints current position and movement options for moving player'''
        x,y = self.position()
        print(f"Your position ({self.moving_player}) has coordinates ({x},{y})")
        options = self.options(details=True)
        print(f"Your options are: {', '.join(options(details=True))}")
       
    def check_for_winner(self) :
        '''checks to see if the moving player has won, returning True if so, False otherwise'''
        x, y = self.position()
        if self.moving_player == "Player 1" :
            winning_row = 8
        else :
            winning_row = 0
        if y == winning_row :
            return(True)
        else :
            return(False)

    def game_over(self) :
        '''here's what we do in the situation that a game is won'''
        print("Game over")

    def move(self, direction) :
        '''this method moves the player in the desired direction'''
        if direction in self.options(details=True) :
            x,y = self.position()
            for component in direction :
                if component == 'U' :
                    x = x
                    y += 1
                elif component == 'D' :
                    x = x
                    y += -1
                elif component == 'L' :
                    x += -1
                    y = y
                elif component == 'R' :
                    x += 1
                    y = y
                else :
                    print("This eventuality is impossible.")
            
            self.current_positions[self.moving_player] = [y,x]
            if self.check_for_winner() == True :
                self.game_over()
            else :
                pass
            self.check_if_adjacent()
            self.swap_perspective()
            self.no_of_moves += 1
            
        else :
            print("This is not a legal move on the current board.")
            return(False)

    def place_fences(self, changes, reverse=False) :
        '''given an encoded set of changes representing fence placement, the board, 
        and a boolean parameter called 'reverse', either place or remove fences accordingly'''
        #note: this is an internal function, so only to be used behind the scenes
        if reverse == False :
            boolean = 0
        else :
            boolean = 1
        #boolean represents whether we want to turn 'ON' of 'OFF' the electric fences (1, 0 resp.)
        orientation = changes[0]
        #note: changes is a list of 0. orientation, 1-4: the squares that need to be changed
        #order of squares given is bottom-left, top-left, top-right, bottom-right
        if orientation == True :  #ie horizontal fence
            directions = ['U', 'D', 'U', 'D']
        elif orientation == False : #ie vertical fence
            directions = ['R', 'R', 'L', 'L']

        for points, direction in zip(changes[1:], directions) :
            x,y = points
            self.board[y][x][direction] = boolean
    
    def move_positions(self, pos, direction) :
        '''this is used to help figure out if we're trapped: consider using it throughout the code
        for further simplicity'''
        x, y = pos
        if direction == 'U' :
            x = x
            y = y+1
            return([x, y])
        elif direction == 'D' :
            x = x
            y = y-1
            return([x, y])
        elif direction == 'L' :
            x = x-1
            y = y
            return([x, y])
        elif direction == 'R' :
            x = x+1
            y = y
            return([x, y])

    def is_trapped(self, player) :
        
        start_temp = self.current_positions[player]
        y, x = start_temp
        if player == "Player 1" :
            destination = [0,8]
        elif player == "Player 2" :
            destination = [0,0]
        visited_cells = [[x,y]]
        current_cells = [[x,y]]
        while destination not in visited_cells and len(current_cells) > 0:
            current_cells_temp = [cells for cells in current_cells]
            for cell in current_cells :
                options = self.options(position = cell)
                for direction in options :
                    pos = self.move_positions(cell, direction)
                    if pos in visited_cells :
                        continue
                    else :
                        visited_cells.append(pos)
                        current_cells_temp.append(pos)
                current_cells_temp.remove(cell)
            current_cells = current_cells_temp
        if len(current_cells) == 0 :
            return(True)
        elif destination in visited_cells :
            return(False)

    def fence(self, location) :
        #location comes in the form of 4 squares and a horizontal/vertical parameter
        #for sake of ease we will represent this with the botttom left square and hor=True or hor=False
        #so location will be a tuple
        #therefore it's necessary to note that the path we are blocking must not already be blocked
        #and it's not possible to criss cross the fences so we need to make sure this isn't a problem
        #okay so we're going to imagine the location = (bottom-corner, hor_bool)
        coordinates, orientation = location
        x1, y1 = coordinates
        x_right, y_right = x1+1, y1
        x_up, y_up = x1, y1+1
        if orientation == True : #ie horizontal
            if self.board[y1][x1]['U'] == 1 and self.board[y_right][x_right]['U'] == 1 :
                if self.board[y1][x1]['R'] == 0 and self.board[y_up][x_up]['R'] == 0 :
                    #failed the check here for crisscrossing
                    print("This is not a legal move as fences cannot criss-cross")
                    return(False)
                else :
                    pass
            else :
                #these fences are already there
                print("This is not a valid move as there are already fences here.")
                return(False)
        
        elif orientation == False : #ie vertical
            if self.board[y1][x1]['R'] == 1 and self.board[y_up][y_up]['R'] == 1 :
                #passed check that it's not already blocked off by fences
                if self.board[y1][x1]['U'] == 0 and self.board[y_right][x_right]['U'] == 0 :
                    #failed the check here that crisscrosses
                    print("This is not a legal move as fences cannot criss-cross")
                    return(False)
                else :
                    pass 
            else :
                #there are already fences there
                print("This is not a valid move as there are already fences here.")
                return(False)
        changes = [orientation, [x1, y1], [x_up, y_up], [x_right, y_right], [x1+1, y1+1]]
        self.place_fences(changes)
        #place fences (preliminary attempt)
        #now it's necessary to check if a player has been 'trapped' (which is an illegal move)
        if self.is_trapped("Player 1") or self.is_trapped("Player 2") :
            self.place_fences(changes, reverse=True)
            print("This is an illegal move as it fences one of the players in. Fences were not placed.")
            return(False)
            
        else :
            self.no_of_moves += 1
            self.fences_dict[self.moving_player] += -1
            self.swap_perspective()
            return(True)

    # def restart(self) :

    # def report_a_problem(self) :
        
game = Quoridor("Ash", "Emma")
game.move('L')
game.move('R')
#etcera