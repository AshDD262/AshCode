import numpy as np
import random

class Quoridor() :
    no_of_players = 2
    first_player = random.choice(["Player 1", "Player 2"])
    moving_player = first_player
    if first_player[-1] == "1" :
        waiting_player = f"{first_player[:-1]}2"
    elif first_player[-1] == "2" :
        waiting_player = f"{first_player[:-1]}1"
    players_adjacent = False
    no_of_moves = 0
    rules = "Rules:"
    fences = dict([["Player 1", 10],["Player 2", 10]])
    start_positions = dict([["Player 1", [0,4]],["Player 2", [8,4]]])
    current_positions = start_positions
    board = np.array([[dict([['U', 1], ['D', 1], ['L', 1],['R',1]]) for x in range(9)] for y in range(9)])
    for counter in range(9) :
        board[8][counter]['U'] = 0
        board[0][counter]['D'] = 0
        board[counter][0]['L'] = 0
        board[counter][8]['R'] = 0

    def __init__(self, player1, player2) :
        self.names = dict([["Player 1", player1],["Player 2", player2]])
        print(self.rules)
        print(f"Player 1: {player1}")
        print(f"Player 2: {player2}")
        print(f"The first move is to be made by: {self.first_player}")
        self.game_in_progress = True

    def swap_axis(self, direction) :
        '''given a direction on the horizontal axis this will return vertical directions and viceversa'''
        if direction in ['U', 'D'] :
            return(['L', 'R'])
        elif direction in ['L', 'R'] :
            return(['U', 'D'])

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

    def check_if_adjacent(self, details=False) :
        '''checks if players are adjacent each other (ie directly above, below, to the left or to the right)
        if details == True then will return which direction the waiting_player is wrt the moving_player'''
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
        if details == True :
            return(info)
        else :
            return(None)

    def print_positions(self) :
        print(f"{self.moving_player}: ({self.names[self.moving_player]}) has position {self.position()}")
        print(f"{self.waiting_player}: ({self.names[self.waiting_player]}) has position {self.position(player='waiting')}")

    def options(self, position = self.position(), details = False) :
        '''returns the set of legal moves that can be made by the moving player on the current board
        if details == True then it considers adjacent pawn complications'''
        x,y = position
        options = [direction for direction, boolean in self.board[y][x].items() if boolean == 1]
        if details == False :
            #no consideration of adjacent pawns requested
            return(options)
        else :
            adjacent_check = self.check_if_adjacent(details=True)
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
        x, y = self.position()
        if self.moving_player == "Player 1" :
            winning_row = 8
        else :
            winning_row = 0
        if y == winning_row :
            return(True)
            print("Winner!!!!!!!")
        else :
            return(False)

    def game_over() :
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
                print("game over!")
            else :
                pass
            self.check_if_adjacent()
            self.swap_perspective()
            self.no_of_moves += 1
            
        else :
            print("This is not a legal move on the current board.")
            return(False)

    def place_fences(self, changes, board, reverse=False) :
        if reverse == False :
            boolean = 0
        else :
            boolean = 1
        orientation = changes[0]
        if orientation == True : 
            directions = ['U', 'D', 'D', 'U']
        elif orientation == False :
            directions = ['R', 'R', 'L', 'L']

        for points, direction in zip(changes[1:], directions) :
            x,y = points
            board[y][x][direction] = boolean

    
    def check_possible(self, board) :
        #check for player_1 - winning row is 8
        y_start, x_start = self.current_positions['Player 1']
        y_1, x_1 = y_start, x_start
        while y1 != 8 :
            options = self.options([x1,y1], True)
            if len(options) :
        
        
        

        #check for player_2
        y2, x2 = self.current_positions['Player 2']

        

        
        
        
                


    
    def fence(self, location) :
        #location comes in the form of 4 squares and a horizontal/vertical parameter
        #for sake of ease we will represent this with the ardttom left square and hor=True or hor=False
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
        self.place_fences(changes, self.board)
        if check_possible(self.board) == True :
            self.no_of_moves += 1
            self.fences[moving_player] += -1
            self.swap_perspective()
            return(True)
        else :
            self.place_fences(changes, self.board, reverse=True)
            print("This is an illegal move as it fences one of the players in.")
            return(False)

    # def restart(self) :

    # def report_a_problem(self) :
        


        
        
game = Quoridor("Ash", "Emma")
print("Hello")
