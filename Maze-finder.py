import numpy as np
global board
board = np.array([[dict([['U', 1],['D', 1],['L', 1],['R', 1]]) for a in range(9)] for a in range(9)])
for counter in range(9) :
    board[counter][8]['R'] = 0
    board[counter][0]['L'] = 0
    board[0][counter]['D'] = 0
    board[8][counter]['U'] = 0

def place_fence(board, coordinates, direction) :
    x, y = coordinates
    if direction == 'Horizontal' :
        board[y][x]['U'] = 0
        board[y][x+1]['U'] = 0
        board[y+1][x]['D'] = 0
        board[y+1][x+1]['D'] = 0
    if direction == 'Vertical' :
        board[y][x]['R'] = 0
        board[y][x+1]['L'] = 0
        board[y+1][x]['R'] = 0
        board[y+1][x+1]['L'] = 0

for x in range(2,6) :
    board[4][x]['U'] = 0
    board[2][x]['D'] = 0
    #roof and floor
for y in range(2,5) :
    board[y][2]['L'] = 0
    board[y][5]['R'] = 0
    #sides!!


def move(pos, direction) :
    x,y = pos
    if direction == 'U' :
        return([x,y+1])
    elif direction == 'D' :
        return([x,y-1])
    elif direction == 'L' :
        return([x-1, y])
    elif direction == 'R' :
        return([x+1, y])


starting_position = [2,4]
x, y = starting_position
x1 = x
y1 = y
destination = [0,8]
visited_cells = [starting_position]
current_cells = [starting_position]
options = [available for available, boolean in board[y1][x1].items() if boolean == 1]
while destination not in visited_cells and len(current_cells) > 0 :
    current_cells_temp = [cells for cells in current_cells]
    for cell in current_cells :
        x, y = cell
        options = [available for available, boolean in board[y][x].items() if boolean == 1]
        for direction in options :
            pos = move(cell, direction)
            if pos in visited_cells :
                continue
            else :
                visited_cells.append(pos)
                current_cells_temp.append(pos)
        current_cells_temp.remove(cell)
    current_cells = current_cells_temp
if len(current_cells) == 0 :
    print("Trapped!")
if destination in visited_cells :
    print("Escaped!")


        


#managed it!! cos we have escaped the loop



