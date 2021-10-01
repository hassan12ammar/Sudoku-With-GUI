# Sudoku
# each row contain all numbers from 1 to 9 without repeating
# each column contain all numbers from 1 to 9 witoput repeating
# box formed of 3X3 square there is 9 boxes in the game
# each box has same rulls as columns and rows

from os import path
import tkinter as tk
from tkinter.constants import DISABLED, TOP
import json

boards_file = open("./boards.json")
boards = json.load(boards_file)
boards_file.close()
boards_length = len(boards)


def get_board_solution(level):

    board = boards[level]["board"]
    SOLUTION = boards[level]["solution"]

    # make dictionary to our box so we can check later on it
    # it has keys: 0-8 
    # values: for column: (start, end) & row: (thre rows that in box)
    deict_index = 0
    BOX_DICT = {}
    for row_index_board in range(0,len(board),3):
        end = 3
        for start in range(0,9,3):
            currint_box_list = []
            for row in range(row_index_board,row_index_board + 3):
                currint_list = board[row][start:end]
                for number in currint_list: currint_box_list.append(number)
                if deict_index not in BOX_DICT.keys(): BOX_DICT[deict_index] = [start,end]
                BOX_DICT[deict_index].append(row)
            deict_index += 1
            end += 3
    return board, SOLUTION, BOX_DICT

def play_window(level):
    global board, SOLUTION, BOX_DICT
    board, SOLUTION, BOX_DICT = get_board_solution(level)
    # make the main window 
    global window
    window = tk.Tk()
    window.title(f"Soduko {level}")
    # set size and position of the window
    WINDOW_WIDTH = 600
    WINDOW_HEIGHT = 450
    # get dimantions of screen
    SCREEN_WIDTH = main_window.winfo_screenwidth()
    SCREEN_HEIGHT = main_window.winfo_screenheight()
    # compute the right posiytton to be in the middle
    POSITION_X = int(SCREEN_WIDTH/2 - WINDOW_WIDTH/2)
    POSITION_Y = int(SCREEN_HEIGHT/2 - WINDOW_HEIGHT/2 -100)
    window.geometry(f'{WINDOW_WIDTH}x{WINDOW_HEIGHT}+{POSITION_X}+{POSITION_Y}')
    # change baground
    window.config(bg = STRONG_ORANGE)
    global buttons_list
    # create the buttons in list has same index as our board and has text from it
    buttons_list = []
    for board_row in board:
        buttons_column = []
        board_list_index = board.index(board_row)
        for board_column in range(len(board_row)):
            button_text = board_row[board_column]
            VERY_DARK_BLUE = "#17202a"
            buttons_column.append(tk.Button(window,text = button_text, bg = VERY_DARK_BLUE,
                                command=lambda id = (board_list_index,board_column): pass_to_play(id) ))
            # disable buttons that alrady played
            if board_row[board_column] != 0: buttons_column[-1]["state"] = DISABLED
        buttons_list.append(buttons_column)

    # place the buttons in nice away 
    index_row = 0
    for row in range(9):
        index_column = 0
        for column in range(9):
            current_button = buttons_list[index_row][index_column]
            # make padding from right and left
            if column == 0:
                current_button.grid(row=row, column=column,padx=(35, 0))  # Left
            elif column == 8:
                current_button.grid(row=row, column=column,padx=(0, 35))  # Right
            # for the boxes
            elif column %3 == 0:
                current_button.grid(row=row, column=column,padx=(2, 0))   #Left

            # make padding from top bottom 
            if row == 0 or (row == 0 and column == 0):
                current_button.grid(row=row, column=column,pady=(35, 0))  # Bottom
            elif row == 8:
                current_button.grid(row=row, column=column,pady=(0, 35))  # Top
            # make padding for the boxes
            elif row %3 == 0 or (row %3 == 0 and column %3 == 0):
                current_button.grid(row=row, column=column,pady=(2, 0))   # Top

            # place other buttons without pading
            else:
                current_button.grid(row=row, column=column)
            current_button.config(height = 2, width = 4)
            index_column += 1
        index_row +=1

# make the main window 
main_window = tk.Tk()
main_window.title("Soduko")
# set size and position of the window
MAIN_WINDOW_WIDTH = 250 + (boards_length ** 2)
MAIN_WINDOW_HEIGHT = 135 + (boards_length ** 2)
# get dimantions of screen
SCREEN_WIDTH = main_window.winfo_screenwidth()
SCREEN_HEIGHT = main_window.winfo_screenheight()
# compute the right posiytton to be in the middle
MAIN_POSITION_X = int(SCREEN_WIDTH/2 - MAIN_WINDOW_WIDTH/2)
MAIN_POSITION_Y = int(SCREEN_HEIGHT/2 - MAIN_WINDOW_HEIGHT/2 -100)
main_window.geometry(f'{MAIN_WINDOW_WIDTH}x{MAIN_WINDOW_HEIGHT}+{MAIN_POSITION_X}+{MAIN_POSITION_Y}')
# change baground
STRONG_ORANGE = "#d35400"
main_window.config(bg = STRONG_ORANGE)

# padx = (rigth, left)  # pady = (top, bottom)
tk.Label(main_window, text = "Choose a Level").grid(row = 0, column = 1, pady = (15,1), padx = (20, 3) )
# make buttons with number of boards we have in our file
row_ = 2
# make pattern 0,1,2 to make the buttons next to each other
column_index_list = [j for i in range(boards_length) for j in range(3)]
# check if we would have one button in the bottom to centerize it
shoud_centerize = boards_length % 3 ==1
for column_index_ in range(boards_length):
    boards_level = list(boards.keys())
    level = boards_level[column_index_]
    column = column_index_list[column_index_]
    if shoud_centerize and column_index_ == boards_length-1 :
        column += 1

    level_button = tk.Button(main_window, text = level, command = lambda level = level: play_window(level))
    level_button.grid(row = row_, column = column , padx = (25, 2), pady = (15,1))
    if column == 2:
        row_ += 2


def get_mouse_position(window_):
    mouse_x = window_.winfo_pointerx() - window_.winfo_rootx()
    mouse_y = window_.winfo_pointery() - window_.winfo_rooty()
    return mouse_x, mouse_y


# make a nice message box :)
def messagebox_info(title,text):
    global my_messagebox
    my_messagebox = tk.Toplevel()
    my_messagebox.title(title)
    # set size and position of the window
    MESSAGEBOX_WIDTH = 250
    MESSAGEBOX_HEIGHT = 100
    # compute the right posiytton to the the button to be on the user curser
    mouse_x,mouse_y = get_mouse_position(my_messagebox)
    MESSAGEBOX_POSITION_X = int(mouse_x - MESSAGEBOX_WIDTH/2)
    MESSAGEBOX_POSITION_Y = int(mouse_y - MESSAGEBOX_HEIGHT/2 - 33)
    my_messagebox.geometry(f"{MESSAGEBOX_WIDTH}x{MESSAGEBOX_HEIGHT}+{MESSAGEBOX_POSITION_X}+{MESSAGEBOX_POSITION_Y}")
    # make label with the text 
    message_label = tk.Label(my_messagebox,text= text )
    message_label.config(font=("Courier", 12), pady = 10)
    message_label.pack()
    # make button to destroy the box
    message_button = tk.Button( my_messagebox, text= "OK", command = lambda:my_messagebox.destroy() )
    message_button.pack(pady = 10)


def check_win(input_number, row, column):
    # check if the number betwen 1-9
    ALOWED_NUMBER = [1, 2, 3, 4, 5, 6, 7, 8, 9]
    if input_number not in ALOWED_NUMBER:
        messagebox_info("Wrong input","The Number You enterd Not Allwoed \n Make sure You enter number \n from 1 to 9 or 0 to empty")
        return False

    # check if any number ar repeted in same row
    # replace old number with our input and check the row
    check_row = board[row].copy()
    check_row[column] = input_number

    check_row_list = []
    for i in check_row:
        # except 0 becaus it's defult as empty
        if i in check_row_list and i != 0:
            messagebox_info("Wrong Answear",f"check rows of {row + 1}, {column + 1}")
            return False
        check_row_list.append(i)

    # check if any number repeted in same column
    # get the column of our input
    check_column = []
    for row_index_ in range(len(board)):
        copy_row = board[row_index_].copy()
        current_column = copy_row[column]
        check_column.append(current_column)

    # replace old number with our input and check the column
    check_column[row] = input_number
    check_column_list = []
    for i in check_column:
        # except 0 becaus it's defult as empty
        if i in check_column_list and i != 0:
            messagebox_info("Wrong Answear",f"check columns of {row + 1}, {column + 1}")
            return False
        check_column_list.append(i)

    # check if any number repeted in same box
    # BOX_DICT values: start,end of columns and rows(3) in list, keys: from 0-8

    # get input box information (start,end,three rows)
    for dict_key in BOX_DICT.keys():
        list_dict = BOX_DICT[dict_key]
        start, end, row_1, row_2, row_3 = list_dict
        row_equality = [row == row_1, row == row_2, row == row_3]
        column_equality = (column > start and column < end) or (column == start) 
        if any(row_equality) and (column_equality):
            start, end, row_1, row_2, row_3 = BOX_DICT[dict_key]
            break
    # get list of box columns that our input in
    list_row_1 = board[row_1][start:end].copy()
    list_row_2 = board[row_2][start:end].copy()
    list_row_3 = board[row_3][start:end].copy()
    input_box_list = [list_row_1, list_row_2, list_row_3]
    # make our list of lists into one list
    input_box = [number for row_box in input_box_list for number in row_box]

    # replace old number with our input and check the box
    input_index = input_box.index(board[row][column])
    input_box[input_index] = input_number

    check_box_list = []
    for i in input_box:
        # except 0 becaus it's defult as empty
        if i in check_box_list and i != 0:
            print("i: ",i)
            print("Box: ",dict_key)
            messagebox_info("Wrong Answear",f"check box of {row + 1}, {column + 1}")
            return False
        check_box_list.append(i)

    return True


def insert_val(entry, id_, entary):
    input_number = int(entry.get())
    entary.destroy()

    row, column = id_
    # check if number is zero so that we reset the button to zero
    if input_number == 0:
        board[row][column] = input_number
        buttons_list[row][column].config(text = input_number)
    # game logic
    else:
        # check if the input is correct 
        move_valid = check_win(input_number, row, column)
        # if it is valid than change button test to the input 
        if move_valid:
            board[row][column] = input_number
            buttons_list[row][column].config(text=input_number)
            # and disable the button if it's same as our solution
            if SOLUTION[row][column] == input_number:
                buttons_list[row][column]["stat"] = DISABLED
                DARK_BLUE = "#243341"
                buttons_list[row][column].config(bg = DARK_BLUE)
                print(True)
            else:
                print(True,"But Not same our Answer")

        # check if win
        win = True
        for Row in board:
            for Column in Row:
                if Row == 0 or Column == 0:
                    win = False
        if win:
            messagebox_info("Win","You Won")

def play(id_):
    # make new window for take and insert the input from user to button if rigth
    entary_window = tk.Toplevel(window)
    # set size and position of the window
    entary_window.title(f"{id_[1]+1}, {id_[0]+1}")
    ENTARY_WINDOW_WIDTH = 250
    ENTARY_WINDOW_HEIGHT = 150
    # compute the right posiytton to be on the user curser
    mouse_x,mouse_y = get_mouse_position(entary_window)
    # consider our hight and width compute the right position
    EN_POSITION_X = int(mouse_x - ENTARY_WINDOW_HEIGHT/2) 
    EN_POSITION_Y = int(mouse_y - ENTARY_WINDOW_HEIGHT/2) 
    # set the geomatry of the window
    entary_window.geometry(f"{ENTARY_WINDOW_WIDTH}x{ENTARY_WINDOW_HEIGHT}+{EN_POSITION_X}+{EN_POSITION_Y}")
    # change window's color
    mostly_black_blue = "#17202a"
    entary_window.config(bg = mostly_black_blue)

    entry = tk.Entry(entary_window)
    # change size of entary and pading
    entry.pack(pady = 14, ipadx = 15, ipady = 10)
    # make button to get insert the input or 
    tk.Button(entary_window, text = "Insert", command= lambda:insert_val(entry, id_, entary_window)).pack(pady = 10)

def pass_to_play(id__):
    play(id__)

if __name__ == "__main__":
    main_window.mainloop()
