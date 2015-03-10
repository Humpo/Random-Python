from pprint import PrettyPrinter
from copy import deepcopy
#^IMPORTS
def insert_vals(certain_vals, board):
    '''
    inserts selected values in certain coords by digit
    returns board dict with 
    '''
    for digit in certain_vals:
        board[digit]+=certain_vals[digit]
    return(board)
def print_board(board, out):
    '''
    Takes board input in dictionary format
    {value1:[(x1, y1),(x2,y2)],
    value2:[(x1, y1),(x2,y2)],
    ...
    }
    prints sudoku board in 9x9 grid using prettyprint
    '''
    sudoku_board = [[[] for i in range(9)]for i in range(9)]#creates 9x9x1 list array
    for number in board:#selects coord and appends number
        for coords in board[number]:
            sudoku_board[coords[0]][coords[1]].append(number)
            
    for row in range(len(sudoku_board)):#any empty spaces are given 0 value
        for column in range(len(sudoku_board[row])):
            if sudoku_board[row][column] == []:sudoku_board[row][column].append(0)

    out.pprint(sudoku_board)#prints sudoku board and extra space
    print()
def repeated_coords(board):
    '''
    boolean return
    uses set data structure to eliminate repeated values
    difference in length means repeated coords
    '''
    all_locations = sum([i for i in board.values()], [])#returns just locations of the board that are filled
    if len(all_locations)>len(set(all_locations)):#check length difference to insure no repeated or error is raised
        return True
    return False
def find_big_box(coord):
    '''
    finds the box a coordinate is in
    returns the range the coord in in
    work in tandum with box_generator
    '''
    x = None
    y = None
    if coord[0]<3:x = range(0,3)
    elif 2<coord[0]<6:x = range(3,6)
    elif 5<coord[0]<9:x = range(6,9)

    if coord[1]<3:y = range(0,3)
    elif 2<coord[1]<6:y = range(3,6)
    elif 5<coord[1]<9:y = range(6,9)

    return ((x,y))
def possible_values(board):
    '''
    returns potential values by looping through empty coordinates
    checking if they exist on the board
    reduces set(1-9) by elements in row, col, and box
    '''
    potential_vals = {}
    all_locations = sum([i for i in board.values()], [])#all locations of values
    for x in range(9):
        for y in range(9):
            if (x, y) not in all_locations:#when a position has no element
                elements_in_row = []
                elements_in_col = []
                elements_in_box = []
                box_range = find_big_box((x, y))
                for num in board:
                    for location in board[num]:
                        if location[0]==x:
                            elements_in_row.append(num)
                        elif location[1]==y:
                            elements_in_col.append(num)
                        elif location[0] in box_range[0] and location[1] in box_range[1]:
                            elements_in_box.append(num)
                potential_vals[(x,y)] = set([i for i in range(1,10)]) - set(elements_in_row) - set(elements_in_col) - set(elements_in_box)
            else:continue
    return potential_vals
def box_generator(box, coord):
    '''
    given the ranges of the box (range(x1,x2),range(y1,y2)) and coord (x,y)
    every next iteration will return a coordinate inside the box except itself 
    '''
    for row in box[0]:
        for col in box[1]:
            if row == coord[0] and col == coord[1]:continue#skips over self
            yield tuple([row,col])#returns coordinates
def find_dig_in_board(board, coord):
    '''
    Takes board input in dictionary format
    innaficient way of searching for the digit but algorithically is needed
    returns digit if coordinate is within dict
    '''
    for dig in board:
        if coord in board[dig]:return dig
    return None
def analyze_possibles(potential_vals, board):
    '''
    get's the certain values to place on the board by reducing total set(1-9) for each empty coordinate.
    reduces set(1-9) by subtracting potential values from empty row,col
    and box coordinates.
    
    enhances possible values in that empty coord in order to check for errors and assure
    that the board that was given is possible to solve
    '''
    if filled_check(board):return 'Invalid'#This statement makes sure that incase a board is filled with incorrect values it will go back up the guessing tree
    vals_set = {}#Return dict that containes values that are certain and correct to insert
    all_coords = sum([i for i in board.values()], [])#existing coords that are filled
    for coord in potential_vals:
        vals = set(potential_vals[coord])#all possible values based on coordinate
        ########reducing sets and enhancing sets
        vals_row = vals.copy()
        vals_col = vals.copy()
        vals_box = vals.copy()
        vals_row_chk = vals.copy()
        vals_col_chk = vals.copy()
        vals_box_chk = vals.copy()
        ########
        box_num = box_generator(find_big_box(coord), coord)#iterator that returns another box coord value except original coord
        for rowcol_elem in range(9):
            '''
            Simultanious loop which checks every next element in the row,col, and box
            '''
            check_row = (coord[0],rowcol_elem) in all_coords#True if the coordinate is filled on the board
            check_row_repeated = (coord[0],rowcol_elem)==coord#True if searching coord is the same as selected coord
            if check_row_repeated:None#if the searching coordinate is itself then do nothing
            elif check_row:#if the coord is filled union to enhance set
                vals_row_chk|=set([find_dig_in_board(board, (coord[0],rowcol_elem))])#enhances set even if coordinate is filled
            else:#if empty and not itself
                vals_row-=set(potential_vals[(coord[0],rowcol_elem)])#reduce set
                vals_row_chk|=set(potential_vals[(coord[0],rowcol_elem)])#enhace set
            #^Checks all the row potential elements

            #each block follows same procedure as code block above
            check_col = (rowcol_elem,coord[1]) in all_coords
            check_col_repeated = (rowcol_elem,coord[1])==coord
            if check_col_repeated:None
            elif check_col:
                    vals_col_chk|=set([find_dig_in_board(board, (rowcol_elem,coord[1]))])
            else:
                vals_col-=set(potential_vals[(rowcol_elem,coord[1])])
                vals_col_chk|=set(potential_vals[(rowcol_elem,coord[1])])
            #^Checks all the col potential elements

            try:#try-except to make sure StopIteration error wont crash program
                box_coord = next(box_num)#Get's the next box coordinate
                if box_coord not in all_coords:
                    vals_box -= set(potential_vals[box_coord])
                    vals_box_chk |= set(potential_vals[box_coord])
                else:
                    vals_box_chk |= set([find_dig_in_board(board, box_coord)])
            except StopIteration:box_coord=set()
            #^Checks all the box potential elements and not
        if vals_box_chk!=vals_col_chk!=vals_row_chk!= set([i for i in range(1,10)]):return("Invalid")#returns invalid if all possible values dont equal a total set(1-9)
        if len(vals_row)==1:vals_set.setdefault(min(vals_row),[]).append(coord) 
        elif len(vals_col)==1:vals_set.setdefault(min(vals_col),[]).append(coord)
        elif len(vals_box)==1:vals_set.setdefault(min(vals_box),[]).append(coord)
        #^adds respective values to dictionary that adds the numbers to the board
    return(vals_set)
def filled_check(board):
    '''
    returns boolean
    checks if the board has 9 associated coords to each number
    AKA full board
    '''
    for digit in board:
        if len(board[digit])<9:return False
    return True
def check_if_solved(board):
    '''
    checks if the board is solved by reducing set(0-9)
    makes sure digit has 0-9 x coords and 0-9 y coords
    '''
    if repeated_coords(board):
        return("Repeated Coordinates on board")
    if filled_check(board):#makes sure board is filled and has no repeated coordinates
        for digit in board:
            if len(board[digit])<9:return(False)
            digx = set([i for i in range(0,9)])
            digy = digx.copy()
            for coord in board[digit]:
                digx-=set([coord[0]])
                digy-=set([coord[1]])
            if digx!=digy!={}:return(False)
        return(True)
    return(False)
def main(board):
    out = PrettyPrinter(indent=4)#neat print instance for debugging
    guess=0#initial guesses 
    guess_tree = {}#dictionary guess tree for potential values
    board_tree = {}#saves previous boards
    potential_vals_flag = False
    check = check_if_solved(board)#initial check
    while not check:
        print_board(board, out)#prints the board to screen
        
        if potential_vals_flag == True:potential_vals = guess_tree[guess];potential_vals_flag = False
        else:potential_vals = possible_values(board)#returns potential values by coordinate
        #^Ensure that when going back up decision tree, potential values minus guessed values are used
        
        certain_vals = analyze_possibles(potential_vals, board)#returns certain values by digit

        #out.pprint(potential_vals)#debugging print values
        #out.pprint(certain_vals)#debugging print values

        #goes back up the descision tree
        if certain_vals=="Invalid":#if invalid followig statements will revert board to a previous condition
            if guess<=0:print("Invalid board, impossible to solve");break#ends program if no guesses and impossible
            else:
                print("Bad Guess, backing to a previous board")#makes user aware
                guess-=1
                board = board_tree[guess]#reverts board to original state
                potential_vals_flag = True#flag allows old potential values to be used
                
        elif certain_vals=={}:
            #create the decision tree
            board_tree[guess] = deepcopy(board)
            guess_tree[guess] = deepcopy(potential_vals)
            guess_coord = next(iter(potential_vals.keys()))#gets a coord
            guess_value = guess_tree[guess][guess_coord].pop()#pops the first value as a guess
            guess+=1#add another guess
            board = insert_vals({guess_value:[guess_coord]}, board)
            print("Guess Scenario")
            print("Guess value: "+str(guess_value))
            print("Coordinate: "+str(guess_coord))
        else:
            board = insert_vals(certain_vals, board)#inserts values and returns new board

        check = check_if_solved(board)#checks if the board is solved
        input("Hit Enter for next decision:")
    if check!=True:
        print(check)
    elif certain_vals!="Invalid":
        print("Solved")
        print_board(board,out)#prints the board to screen
    else:
        print("Uh-oh")
if __name__=="__main__":
    '''
    If you want to input board follow format
    value:[(x1, y1),(x2,y2)]
    for refrence (0,0) refers to the top most left box
    (0,8) refers to the top most right box
    etc...
    This is the most efficent way to store
    the board with the smallest amount of memory

    If board is unsolvable the program will tell you.
    This can mean that the board was entered improperly

    Possible Errors:
    "Invalid board, impossible to solve"
    "Repeated Coordinates on board"

    Program will crash if the board is not in the right format

    CAUTION:
    If an additional value on the board is played by mistake the board
    might still be solvable.

    MAKE SURE THE BOARD IS ENTERED CORRECTLY!!!!!!!!!!!!!!!!!!
    '''
    #############INSERT BOARD HERE###############
    #############################################
    board = {
        #value:[(x1, y1),(x2,y2)],
        1:[(1,0),(5,7),(6,5)],
        2:[(2,6),(7,2)],
        3:[(2,4),(8,6)],
        4:[(2,3),(5,6),(8,1)],
        5:[(4,3),(7,7)],
        6:[(3,8)],
        7:[(0,3)],
        8:[(5,8),(6,4)],
        9:[(4,5)]
        }
    #############################################
    #############################################
    main(board)
