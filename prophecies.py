# 550 lines of messy code
# also tkinter sucks

from tkinter import *
from tkinter import messagebox
from tkinter.font import Font
import random
from time import perf_counter

# most important function
def print_board(board):
    print('='*(6 + N * 5))
    for i in range(N):
        print('|| ',end='')
        for j in range(N):
            v = board[index1d[i][j]]
            if len(v) == 0: print("  X  ",end='')
            elif not v.isdigit(): print(" "*(4 - len(v)) + v + " ",end='')
            else: print("  .  ",end='')
        print(" ||\n")
    print('='*(6 + N * 5))

#helper function, dont worry about it
def remove_val(x, v):
    if not v.isdigit(): return x
    i = x.find(v)
    if i == -1: return x
    res = x[:i] + x[i+1:]
    return res

#self explanatory
def possible_moves(board):
    return [(ind, val) for ind, value in enumerate(board) if value.isdigit() and len(value) > 0 for val in value + 'X']

# self explanatory as well    
def make_move(board, i, j, x, ptoken):
    board = board[:]
    v = board[(ind := index1d[i][j])]
    if len(v) == 0 or not v.isdigit() or (x not in v and x != 'X'): return None
    if x == 'X': 
        board[ind] = ""
        return board
    board[ind] = ptoken + x + ptoken
    for x1 in range(N):
        if x1 != i: 
            board[index1d[x1][j]] = remove_val(board[index1d[x1][j]], x)
    for x2 in range(N):
        if x2 != j:
            board[index1d[i][x2]] = remove_val(board[index1d[i][x2]], x)
    return board

# game over and final score function            
def game_over(board):
    for x in board:
        if x.isdigit(): return None

    p1 = p2 = 0
    for i in range(N):
        count = 0
        for j in range(N):
            if len(board[index1d[i][j]]) != 0:
                count += 1
        count = str(count)
        for j in range(N):
            if count in (v := board[index1d[i][j]]):
                if ptoken_inv_dict[v[0]] == 1: p1 += int(count)
                else: p2 += int(count)
                break
    
    for j in range(N):
        count = 0
        for i in range(N):
            if len(board[index1d[i][j]]) != 0:
                count += 1
        count = str(count)
        for i in range(N):
            if count in ((v := board[index1d[i][j]])):
                if ptoken_inv_dict[v[0]] == 1: p1 += int(count)
                else: p2 += int(count)
                break
    return (p1, p2)

# cursed 60 line eval function: DONT LOOK!
def eval_board(board):
    score = 0
    for i in range(N):
        row_score = row_sum = 0
        blank = blocked = filled = 0
        fbp1, fbp2 = set(), set()
        for j in range(N):
            x = board[index1d[i][j]]
            if x.isdigit(): blank += 1
            elif len(x) == 0: blocked += 1
            else:
                filled += 1
                if ptoken_inv_dict[x[0]] == 1: fbp1.add(x[1:-1])
                else: fbp2.add(x[1:-1])
        s1 = N - (blocked + blank * formula)
        #s2 = M - (blocked + max(0, M * formula - blocked))
        if blank == 0: 
            if str(filled) in fbp1: score += filled
            if str(filled) in fbp2: score -= filled
            continue
        for pos in range(filled, filled+blank+1):
            row_sum += blank - abs(pos - s1)
            if str(pos) in fbp1: row_score += blank - abs(pos - s1)
            if str(pos) in fbp2: row_score -= blank - abs(pos - s1)
        score += row_score / row_sum
    
    for j in range(N):
        col_score = col_sum = 0
        blank = blocked = filled = 0
        fbp1, fbp2 = set(), set()
        for i in range(N):
            x = board[index1d[i][j]]
            if x.isdigit(): blank += 1
            elif len(x) == 0: blocked += 1
            else:
                filled += 1
                if ptoken_inv_dict[x[0]] == 1: fbp1.add(x[1:-1])
                else: fbp2.add(x[1:-1])
        s1 = N - (blocked + blank * formula)
        #s2 = N - (blocked + max(0, N * formula - blocked))
        if blank == 0: 
            if str(filled) in fbp1: score += filled
            if str(filled) in fbp2: score -= filled
            continue
        for pos in range(filled, filled+blank+1):
            col_sum += blank - abs(pos - s1)
            if str(pos) in fbp1: col_score += blank - abs(pos - s1)
            if str(pos) in fbp2: col_score -= blank - abs(pos - s1)
        score += col_score / col_sum
    return round(score * 100)

# self-evident
def make_random_move(board, player, ptoken): 
    ind, x = random.choice(possible_moves(board))
    i, j = index2d[ind]
    make_the_move(i, j, x)

# also obvious
def get_user_move(board, player, ptoken):
    print("ooooooo")

# greedy
def get_aggressive_move(board, p, ptoken):
    global player
    get = max if player == 1 else min
    next_boards = [(make_move(board, index2d[ind][0], index2d[ind][1], x, ptoken), ind, x) for ind, x in possible_moves(board)]
    board, ind, x = get(next_boards, key=lambda x: eval_board(x[0]))
    i, j = index2d[ind]
    make_the_move(i, j, x)


# minimax part 1
def max_step(board, depth, alpha, beta, tm, ab=True): 
    if depth == 0 or perf_counter() - tm > mxtime: return eval_board(board)
    moves = possible_moves(board)
    if len(moves) == 0: return eval_board(board)
    curr_max = float('-inf')
    for ind, val in moves:
        res = min_step(make_move(board, index2d[ind][0], index2d[ind][1], val, ptoken_dict[1]), depth - 1, alpha, beta, tm)
        alpha = max(alpha, curr_max := max(curr_max, res))
        if ab and alpha >= beta: return res
    return curr_max

# minimax part 2
def min_step(board, depth, alpha, beta, tm, ab=True):
    if depth == 0 or perf_counter() - tm > mxtime: return eval_board(board)
    moves = possible_moves(board)
    if len(moves) == 0: return eval_board(board)
    curr_min = float('inf')
    for ind, val in moves:
        res = max_step(make_move(board, index2d[ind][0], index2d[ind][1], val, ptoken_dict[2]), depth - 1, alpha, beta, tm)
        beta = min(beta, curr_min := min(curr_min, res))
        if ab and alpha >= beta: return res
    return curr_min

# uses minimax
def get_good_move1(board, p, ptoken):
    global player
    s, ans, depth = perf_counter(), None, 1
    while perf_counter() - s < mxtime:
        if player == 1: 
            moves = [(min_step(make_move(board, index2d[ind][0], index2d[ind][1], val, ptoken), depth, float('-inf'), float('inf'), s, False), ind, val) for ind, val in possible_moves(board)]
            ans = max(moves)
        else:
            moves = [(max_step(make_move(board, index2d[ind][0], index2d[ind][1], val, ptoken), depth, float('-inf'), float('inf'), s, False), ind, val) for ind, val in possible_moves(board)]
            ans = min(moves)
        depth += 1
    b, ind, val = ans
    i, j = index2d[ind]
    make_the_move(i, j, val)


# uses minimax + alphabeta
def get_good_move2(board, p, ptoken):
    global player
    s, ans, depth = perf_counter(), None, 1
    while perf_counter() - s < mxtime:
        if player == 1: 
            moves = [(min_step(make_move(board, index2d[ind][0], index2d[ind][1], val, ptoken), depth, float('-inf'), float('inf'), s), ind, val) for ind, val in possible_moves(board)]
            ans = max(moves)
        else:
            moves = [(max_step(make_move(board, index2d[ind][0], index2d[ind][1], val, ptoken), depth, float('-inf'), float('inf'), s), ind, val) for ind, val in possible_moves(board)]
            ans = min(moves)
        depth += 1
    b, ind, val = ans
    i, j = index2d[ind]
    make_the_move(i, j, val)


def mtdf(board, f, d, player, s):
    passes = 0
    table = dict()
    g, lower, upper = f, float('-inf'), float('inf')
    while lower < upper:
        passes += 1
        beta = g + 1 if g == lower else g
        g = alpha_beta_with_memory(board, beta - 1, beta, d, table, player, s)
        if g < beta: upper = g
        else: lower = g
        #print(passes, lower, upper)
    #print(passes)
    #if flag: print(len(table), d, f, g, passes)
    return g

def get_good_move3(board, p, ptoken):
    global player
    pans, ans, depth, g1, g2 = None, None, 1, 0, 0
    s = perf_counter()
    while perf_counter() - s < mxtime or pans is not None and abs(pans[0]) > 10**8:
        if player == 1:
            moves = [(mtdf(make_move(board, index2d[ind][0], index2d[ind][1], val, ptoken), g1 if depth % 2 == 1 else g2, depth, nextplayer(player), s), ind, val) for ind, val in possible_moves(board)]
            pans, ans = ans, max(moves)
            if depth % 2 == 0: g1 = ans[0]
            else: g2 = ans[0]
        else:
            moves = [(mtdf(make_move(board, index2d[ind][0], index2d[ind][1], val, ptoken), g1 if depth % 2 == 1 else g2, depth, nextplayer(player), s), ind, val) for ind, val in possible_moves(board)]
            pans, ans = ans, min(moves)
            if depth % 2 == 0: g1 = ans[0]
            else: g2 = ans[0]
        depth += 1
    if pans is None: pans = ans
    b, ind, val = pans
    i, j = index2d[ind]
    make_the_move(i, j, val)


def alpha_beta_with_memory(board, alpha, beta, d, table, player, s): 
    if (tboard := tuple(board)) in table:
        
        l, u = table[tboard]

        if l is not None:
            if l >= beta:
                #print(alpha, beta, l, u, d)
                return l
            alpha = max(l, alpha)
        if u is not None:
            if u <= alpha: 
                #print(alpha, beta, l, u, d)
                return u
            beta = min(u, beta)
    else: table[tboard] = [None, None]
    g, moves = None, possible_moves(board)
    if d == 0 or perf_counter() - s > mxtime: g = eval_board(board)
    elif len(moves) == 0: return eval_board(board) * 10**9
    elif player == 1:
        g, a = float('-inf'), alpha
        for ind, move in moves:
            g = max(g, alpha_beta_with_memory(make_move(board, index2d[ind][0], index2d[ind][1], move, ptoken_dict[player]), a, beta, d - 1, table, nextplayer(player), s))
            a = max(a, g)
            if g >= beta: break
    else:
        g, b = float('inf'), beta
        for ind, move in moves:
            g = min(g, alpha_beta_with_memory(make_move(board, index2d[ind][0], index2d[ind][1], move, ptoken_dict[player]), alpha, b, d - 1, table, nextplayer(player), s))
            b = min(b, g)
            if g <= alpha: break
    if g <= alpha: table[tboard][1] = g 
    elif alpha < g < beta:
        table[tboard][0] = g
        table[tboard][1] = g
    else: table[tboard][0] = g
    return g

# for people who don't know
def print_rules():
    print("\nRules:\n")
    print("1. On each turn, place a number or an X in an availible square (a square that is not already an X) that isn't already there in that row.\n")
    print("2. The number you place is a prediction of how many numbers will eventually appear in that column.\n")
    print("3. At the end of the game, if you correctly predicted the how many numbers would be in a row/column, you get that many points.\n")
    print("4. Highest points wins. Second player wins if there is a tie.\n")


def cellpressed(x):
    i, j = map(int, x.split())
    global curr_b
    if curr_b is not None:
        boardgrid[curr_b[0]][curr_b[1]].config(relief=RAISED, bg="#ffffff", fg="#ffffff")
        if curr_b == (i, j): 
            curr_b=None
            return
    curr_b=(i, j)
    boardgrid[curr_b[0]][curr_b[1]].config(relief=SUNKEN, bg='#bbbbff', fg="#bbbbff")

def get_game_frame(window, N):
    global boardgrid, gameframe, curr_b
    if gameframe is not None: 
        gameframe.pack_forget()
        gameframe.destroy()
        curr_b = None
    
    boardgrid = [[None for _ in range(N)] for __ in range(N)]
    gameframe=Frame(window, relief='solid', bd=2)
    gameframe.pack_propagate(False)

    for i in range(N):
        framei=Frame(gameframe)
        for j in range(N):  
            b = Button(framei, background="#ffffff", command=lambda x = str(i) + " " + str(j):cellpressed(x), font=('Impact', 20), text='0', foreground='#ffffff', activeforeground="#eeeeee", activebackground="#eeeeee")
            b.pack(expand=True, fill=BOTH, side=LEFT)
            boardgrid[i][j] = b
        framei.pack(expand=True, fill=BOTH, side=TOP)

    gameframe.pack(fill=BOTH, expand=True, side=LEFT)

def get_user_input():
    if str(players[player-1]) == str(get_user_move):
        get_move_frame(movereserveframe, N, "Player %s's" % (player))
    else:
        get_next_move_frame(movereserveframe)

def destroymoveframe():
    global moveframe
    if moveframe is not None:
        moveframe.pack_forget()
        moveframe.destroy()

def get_next_move_frame(window):
    global moveframe
    destroymoveframe()
    moveframe = Frame(window)
    Button(moveframe, text="Next Move", font=('Courier New', 15), command=next_move).pack(fill=BOTH, expand=True, anchor=CENTER)
    moveframe.pack()


def get_move_frame(window, N, player):
    global movee, moveframe
    destroymoveframe()
    moveframe=LabelFrame(window, text=player + " Move")
    movee = StringVar()
    moveset = [str(i+1) for i in range(N)] + ['X']
    movemenu = OptionMenu(moveframe, movee, *moveset)
    movemenu.config(font=dropdownfont)
    movemenu.pack(side=LEFT, fill='x', expand=True, padx=20)
    Button(moveframe, text="Confirm Move", font=('Courier New', 14), command=move_confirmed).pack(side=LEFT, fill='x', expand=True, padx=20)
    moveframe.pack(expand=True, anchor=CENTER, ipady=20)

def move_confirmed():
    s = perf_counter()
    global player
    themove = movee.get()
    if len(themove) == 0: 
        messagebox.showerror("Error", "Please choose a move before making move!")
        return
    if curr_b is None:
        messagebox.showerror("Error", "Please choose a square before making move!")
        return
    i, j = curr_b
    make_the_move(i, j, themove)
    next_move()

def make_the_move(i, j, x):
    global board, player
    
    res = make_move(board, i, j, x, ptoken)
    if res is None:
        messagebox.showerror("Error", "Invalid Move. Please try again.")
        player=nextplayer(player)
        return
    board=res
    button = boardgrid[i][j]
    #curr_w = button.winfo_width()
    button.config(text=x, relief=RAISED, state=DISABLED, bg="#ffffff", disabledforeground=pcol_dict[player] if x != 'X' else "#000000", font=('Impact', 20))
    
    #button.config(width=curr_w * (1/6))

def show_rules():
    rules = """1. On each turn, place a number or an X in an available square (a square that is not already an X) that isn't already there in that row.

2. The number you place is a prediction of how many numbers will eventually appear in that column.

3. At the end of the game, if you correctly predicted the how many numbers would be in a row/column, you get that many points.

4. Highest points wins. Second player wins if there is a tie.
    """
    messagebox.showinfo("Rules of the Game", rules)

def how_to_play():
    htp = """1. Choose your parameters and click 'Start Game'. 
    a. For each player, you can select a user, random move generator, or 4 levels of AIs. 
    b. Note that higher level AIs need a higher time limit to show substantial improvement over lower level AIs.

2. If it is the user's turn, press on a square and choose a number from the dropdown for your move. Press 'Confirm Move' to submit your move.

3. If it is the computer's turn, click 'Next Move' to generate the computer's next move.

4. Exit the current game at any time by pressing 'End Game'.

5. Enjoy!
    """
    messagebox.showinfo("How to Play", htp)

def get_options(window):
    global p1choice, p2choice, boardsize, timelimit, confirmbutton
    p1choice, p2choice, boardsize, timelimit=StringVar(),StringVar(),StringVar(),StringVar()
    p1choice.set("User Moves")
    p2choice.set("User Moves")
    boardsize.set("6x6 Normal")
    timelimit.set("5 sec")
    playerframe=Frame(window)

    plr1frm = LabelFrame(playerframe, text="Player 1")
    plr1 = OptionMenu(plr1frm, p1choice, "User Moves", "Random Moves", "AI Level 0", "AI Level 1", "AI Level 2", "AI Level 3")
    plr1.config(font = dropdownfont)
    plr1.pack(fill=BOTH, expand=True)
    plr1frm.pack(expand=True, fill = BOTH, side=LEFT, anchor=CENTER)

    plr2frm = LabelFrame(playerframe, text="Player 2")
    plr2 = OptionMenu(plr2frm, p2choice, "User Moves", "Random Moves", "AI Level 0", "AI Level 1", "AI Level 2", "AI Level 3")
    plr2.config(font=dropdownfont)
    plr2.pack(fill=BOTH, expand=True)
    plr2frm.pack(expand=True, fill = BOTH, side=LEFT, padx=50, anchor=CENTER)

    playerframe.pack(side=TOP, padx=50, pady=40, anchor=CENTER)

    boardtimeframe=Frame(window)

    brdszefrm=LabelFrame(boardtimeframe, text="Board Size")
    brdsze=OptionMenu(brdszefrm, boardsize, "3x3 Trivial", "4x4 Simple", "5x5 Easy", "6x6 Normal", "7x7 Hard", "8x8 Challenging", "9x9 Extreme")
    brdsze.config(font=dropdownfont)
    brdsze.pack(fill=BOTH, expand=True)
    brdszefrm.pack(expand=True, fill=BOTH, side=LEFT, anchor=CENTER)

    timelimitframe=LabelFrame(boardtimeframe, text="Time Limit")
    tmlmt=OptionMenu(timelimitframe, timelimit, "1 sec", "2 sec", "5 sec", "10 sec", "30 sec")
    tmlmt.config(font=dropdownfont)
    tmlmt.pack(fill=BOTH, expand=True)
    timelimitframe.pack(expand=True, fill=BOTH, side = LEFT, padx=50, anchor=CENTER)

    boardtimeframe.pack(side=TOP, anchor=CENTER)

    confirmbutton=Button(window, text="Start Game",font=('Courier New', 14), command=start_game)
    confirmbutton.pack(side=TOP, pady=40)

def set_game():
    global N
    N = int(boardsize.get()[0])
    get_game_frame(boardreserveframe, N)

def end_game(): 
    confirmbutton.config(text='Start Game', command=start_game)
    set_game()
    destroymoveframe()

def start_game(): 
    confirmbutton.config(text='End Game', command=end_game)
    set_game()
    destroymoveframe()
    global formula, index1d, index2d, ptoken_dict, ptoken_inv_dict, formula, mxtime, nextplayer, board, ptoken,players, player, pname_dict, pcol_dict
    # on average, this is the percent of X's per row/column 
    formula = 0.14
    mxtime=int(timelimit.get().split()[0])-0.1

    board = [''.join([str(x+1) for x in range(N)]) for _ in range(N * N)]
    index1d = [[i * N + j for j in range(N)] for i in range(N)]
    index2d = [(x // N, x % N) for x in range(N * N)]

    player=2
    nextplayer = lambda x: 2 if x == 1 else 1
    ptoken_dict, ptoken_inv_dict = {1:'|', 2:'#'}, {'|':1, "#":2}
    pname_dict, pcol_dict = {1: "RED", 2:"BLUE"}, {1: "#ff0000", 2:"#0000ff"}
    player_dict = {"User Moves" : get_user_move, "Random Moves" : make_random_move, "AI Level 0" : get_aggressive_move, "AI Level 1" : get_good_move1, "AI Level 2" : get_good_move2, "AI Level 3" : get_good_move3}
    players = [player_dict[p1choice.get()], player_dict[p2choice.get()]]
    setup_next_move()

def setup_next_move():
    global player, ptoken

    player = nextplayer(player)
    ptoken = ptoken_dict[player]
    gamemessages.config(text="Player %s's turn playing as %s" % (player, pname_dict[player]))
    get_user_input()

def next_move():
    global board, ptoken, player
    
  
    players[player-1](board, player, ptoken_dict[player])
    for ind, x in enumerate(board):
        i, j = index2d[ind]
        if len(x) == 0 and boardgrid[i][j]["state"] != DISABLED:
            boardgrid[i][j].config(text='X', relief=RAISED, state=DISABLED, bg="#ffffff", disabledforeground="#000000")

    if (x := game_over(board)) is not None:
        p1, p2 = x
        gamemessages.config(text="Game Over!\nPlayer %s playing as %s wins. \nScore: %s-%s" % ((pw :=1 if p1 > p2 else 2), pname_dict[pw], p1, p2))
        destroymoveframe()
        return
    setup_next_move()

    


N = boardgrid = gameframe = p1choice = p2choice = boardsize = timelimit = moveframe = movee=  playerturnlabel= confirmbutton=None
formula = index2d= index1d=curr_b = players=ptoken_dict = ptoken_inv_dict= pname_dict=  pcol_dict=nextplayer= mxtime= formula =None
board = ptoken=None




window = Tk()
window.title("Prophecies")
width= window.winfo_screenwidth()
height= window.winfo_screenheight()
window.geometry("%dx%d" % (width-100, height-100))
dropdownfont=Font(family="Courier New", size=11)

Label(window, text="Welcome to Prophecies", font=('Courier New', 40)).pack(side=TOP, pady=5)
howtoplayframe=Frame(window)
Button(howtoplayframe, text='Show Rules', font=('Courier New', 14), command=show_rules).pack(side=LEFT, padx=50)
Button(howtoplayframe, text='How to Play', font=('Courier New', 14), command=how_to_play).pack(side=LEFT)
howtoplayframe.pack(side=TOP, pady=5, anchor=CENTER)
boardreserveframe = Frame(window)
boardreserveframe.pack(fill=BOTH, expand=True, side=LEFT, padx=50, pady=20)

gamemessages = Label(window, font=('Courier New', 20))
gamemessages.pack(side=TOP, pady=20, padx=30)

get_options(window)
gameresultframe=Frame(window)
gameresultframe.pack(fill=BOTH, expand=True, side=BOTTOM, pady=30)
movereserveframe=Frame(window)
movereserveframe.pack(fill=BOTH, expand=True, side=BOTTOM, pady=10)
set_game()


window.mainloop()
