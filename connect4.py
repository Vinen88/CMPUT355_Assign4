from random import shuffle
from numpy import argmax
from copy import deepcopy, copy
class Game_tree:
        board = []
        move = []
        parent = None
        score = 0
        def __init__(self, board):
            self.board = board
    
class Game_board:
    pos = []
    moves = []

    def __init__(self):
        self.pos = [["*" for i in range(7)] for i in range(6)]
    
    def __repr__(self):
        self.print()

    def print(self):
        for row in reversed(self.pos):
            for position in row:
                print(position, end='\t')
            print('\n')
        print("1\t2\t3\t4\t5\t6\t7")
    
    def move(self, position, player):
        for row in range(len(self.pos)):
        #for row in self.pos:
            if self.pos[row][position] == "*":
                self.pos[row][position] = player
                self.moves.append((row,position))
                return False
        return True

    def tree_move(self, position, player, board):
        for row in range(len(board)):
        #for row in self.pos:
            if board[row][position] == "*":
                board[row][position] = player
                return board
        return None

    def build_tree(self, player, parent=None):
        if parent == None:
            board = deepcopy(self.pos)
            root = Game_tree(board)
            root.score = self.check_score("B", root.board)
        else:
            root = parent
        #check root win if root is winning node return.
        if self.check_win("R", root.board) or self.check_win("R", root.board):
            return
        for i in range(7):
            board = deepcopy(root.board)
            new_board = self.tree_move(i, player, board)
            if new_board != False:
                root.move.append(Game_tree(new_board))
            else:
                root.move.append(None)
        for node in root.move:
            node.score = self.check_score("B", node.board)
            node.parent = root 
            self.build_tree("B" if player == "R" else "R", node)
        if parent == None:
            return root

    def build_tree2(self, board, player):
        board2 = deepcopy(board)
        root = Game_tree(board2)
        root.move = []
        for i in range(7):
            board2 = deepcopy(root.board)
            new_board = self.tree_move(i, player, board2)
            if new_board != None:
                root.move.append(Game_tree(new_board))
            else:
                root.move.append(None)
        for node in root.move:
            if node != None:
                node.score = self.check_score(player, node.board)
                #print(node.score)
                node.parent = root
                for i in range(7):
                    board2 = deepcopy(node.board)
                    new_board = self.tree_move(i, "B" if player == "R" else "R", board2)
                    if new_board != None:
                        node.move.append(Game_tree(new_board))
                    else:
                        root.move.append(None)
                for child in node.move:
                    if child != None:
                        child.score = self.check_score(player, child.board)
                        child.parent = node
                        child.parent.score =+ child.score/7
        return root    
            
        

    def remove_move(self):
        move = self.moves.pop()
        self.pos[move[0]][move[1]] = '*'
        return

    def board_full(self):
        total = 0
        size = len(self.pos) * len(self.pos[0])
        for column in self.pos:
            for item in column:
                if item == 'R' or item == 'B':
                    total += 1
        if total == size:
            return True
        return False
    
    def is_empty(self):
        for row in self.pos:
            for column in row:
                if column != '*':
                    return False
        return True

    #i = columns j = rows?
    def check_win(self, symbol, board):
        for i in range(6):
            for j in range(7):
                if board[i][j] == symbol:
                    if (j - 3) >= 0:
                        if (i + 3) <= 5: #5? maybe? check for off by one
                            #check stright up and diagonal up left
                            if board[i+1][j] == symbol and board[i+2][j] == symbol and board[i+3][j] == symbol:
                                return True
                            if board[i+1][j-1] == symbol and board[i+2][j-2] == symbol and board[i+3][j-3] == symbol:
                                return True   
                        #check left I dont think this is needed, we will just need to check right. but whatever.
                        if board[i][j-1] == symbol and board[i][j-2] == symbol and board[i][j-3] == symbol:
                            return True
                    if (j + 3) <= 6: #6? maybe?
                        if(i + 3) <= 5:
                            #check up and up right
                            if board[i+1][j] == symbol and board[i+2][j] == symbol and board[i+3][j] == symbol:
                                return True
                            if board[i+1][j+1] == symbol and board[i+2][j+2] == symbol and board[i+3][j+3] == symbol:
                                return True
                        #check right
                        if board[i][j+1] == symbol and board[i][j+2] == symbol and board[i][j+3] == symbol:
                            return True
        return False
    
    def check_up_score(self, i, j, board, symbol):
        score = 0
        up_checked = 0
        if board[i+1][j] == symbol and board[i+2][j] == symbol and board[i+3][j] == symbol and up_checked == 0:
            score += 1000
            up_checked = 1 
        elif (board[i+1][j] == symbol and board[i+2][j] == symbol and board[i+3][j] == '*') and up_checked == 0:
            if i > 0:
                if board[i-1][j] == symbol:
                    pass
                else:
                    score += 50
                    up_checked = 1
            else:
                score += 50
                up_checked = 1
        elif board[i+1][j] == symbol and board[i+2][j] == '*' and up_checked == 0:
            if i > 0:
                if board[i-1][j] == symbol:
                    pass
                else:
                    score += 10
                    up_checked = 1
            else:
                score += 10
                up_checked = 1
        return score
    
    def check_diag_left(self,i,j,board,symbol):
        score = 0
        if board[i+1][j-1] == symbol and board[i+2][j-2] == symbol and board[i+3][j-3] == symbol:
            score += 1000
        elif (board[i+1][j-1] == symbol and board[i+2][j-2] == symbol and board[i+3][j-3] == '*') or \
            (board[i+1][j-1] == symbol and board[i+2][j-2] == '*' and board[i+3][j-3] == symbol) or \
            (board[i+1][j-1] == '*' and board[i+2][j-2] == symbol and board[i+3][j-3] == symbol):
            if j + 1 <= 6 and i - 1 >= 0:
                if board[i - 1][j + 1] == symbol:
                    pass
                else:
                    score += 50
            else: 
                score += 50   
        elif (board[i+1][j-1] == symbol and board[i+2][j-2] == '*'):
            if j + 1 <= 6 and i - 1 >= 0:
                if board[i - 1][j + 1] == symbol:
                    pass
                else:
                    score += 10
            else: 
                score += 10
        return score  
    
    def check_diag_right(self, i, j, board, symbol):
        score = 0
        if board[i+1][j+1] == symbol and board[i+2][j+2] == symbol and board[i+3][j+3] == symbol:
            score += 1000
        elif (board[i+1][j+1] == symbol and board[i+2][j+2] == symbol and board[i+3][j+3] == '*') or \
            (board[i+1][j+1] == symbol and board[i+2][j+2] == '*' and board[i+3][j+3] == symbol) or \
                (board[i+1][j+1] == '*' and board[i+2][j+2] == symbol and board[i+3][j+3] == symbol):
            if i > 0 and j > 0:
                if board[i - 1][j - 1] == symbol:
                    pass
                else: 
                    score += 50
            else:
                score += 50
        elif board[i+1][j+1] == symbol and board[i+2][j+2] == '*':
            if i > 0 and j > 0:
                if board[i - 1][j - 1] == symbol:
                    pass
                else:
                    score += 10
            else:
                score += 10
        return score
    
    def check_right(self, i, j, board, symbol):
        score = 0
        if board[i][j+1] == symbol and board[i][j+2] == symbol and board[i][j+3] == symbol:
            score += 1000
        elif (board[i][j+1] == symbol and board[i][j+2] == symbol and board[i][j+3] == '*') or \
            (board[i][j+1] == symbol and board[i][j+2] == '*' and board[i][j+3] == symbol) or \
                (board[i][j+1] == '*' and board[i][j+2] == symbol and board[i][j+3] == symbol):
            if j > 0:
                if board[i][j - 1] == symbol:
                    pass
                else:
                    score += 50
            else:
                score += 50
        elif board[i][j+1] == symbol and board[i][j+2] == '*':
            if j > 0:
                if board[i][j - 1] == symbol:
                    pass
                else:
                    score += 10
            else:
                score += 10
        return score

    #this is a beast and is terrible I have no other idea how to do it and too lazy to refactor 
    def check_score(self, symbol, board, first=0):
        if first == 0:
            other_score = self.check_score("B" if symbol == "R" else "R", board, 1)
        score = 0
        #counted = []
        for i in range(6):
            for j in range(7):
                up_checked = 0
                if board[i][j] == symbol:
                    if (j - 3) >= 0:
                        if (i + 3) <= 5: #5? maybe? check for off by one
                            #check stright up and diagonal up
                            if up_checked == 0:
                                score += self.check_up_score(i, j, board, symbol)
                                up_checked = 1
                            #check diagonal left
                            score += self.check_diag_left(i, j, board, symbol)
                    
                    if (j + 3) <= 6: #6? maybe?
                        if(i + 3) <= 5:
                            #check up and up right (need to figure out how not to double add up)
                            if up_checked == 0:
                                score += self.check_up_score(i, j, board, symbol)
                                up_checked = 1

                            #up right
                            score += self.check_diag_right(i, j, board, symbol)
                        #check right
                        score += self.check_right(i, j, board, symbol)
                        
        if first == 1:
            return score
        else:
            return score - other_score

    def print_help(self):
        print("'h' for help")
        print("Red goes first player enters 1-7 to pick which slot to play in")
        print("b to go back a move")
        print("exit to exit")
        print("next to get next move suggestion")

    def random_player(self):
        moves = [1,2,3,4,5,6,7]
        shuffle(moves)
        return str(moves.pop())
    
    def tree_best_move(self, board):
        root = self.build_tree2(board, "B")
        scores = []
        #print(len(root.move))
        for node in root.move:
            if node == None:
                scores.append(-10000)
            else:
                scores.append(node.score)
        max = argmax(scores)  
        print(scores)      
        return str(max+1)

    def suggest_move(self, board):
        root = self.build_tree2(board, "R")
        scores = []
        for node in root.move:
            if node == None:
                scores.append(-10000000)
            else:
                scores.append(node.score)
        max = argmax(scores)
        print("your best move is: "+str(max + 1))

    def two_play_game(self):
        player = 0
        while(not(self.check_win("R", self.pos)) and not(self.check_win("B", self.pos)) and not(self.board_full())):
            self.print()
            if player == 0:
                move = input("Player One Move: ")
            elif player == 1:
                move = input("Player Two Move: ")
            if move == "h":
                self.print_help()
            elif move == "exit":
                exit()
            elif move == "b":
                if self.is_empty():
                    print("Board is empty, please make a move first.\n")
                else:
                    self.remove_move()
            elif move == "s":
                print(self.check_score("R",self.pos))
            else:
                if player == 0:
                    while(self.move(int(move)-1, 'R')):
                        move = input("Player One Move Again(Invalid Position): ")
                    player = 1
                elif player == 1:
                    while(self.move(int(move)-1, 'B')):
                        move = input("Player Two Move Again(Invalid Position): ")
                    player = 0
        if self.check_win("R", self.pos):
            self.print()
            print("RED WINS!!")
        elif self.check_win("B", self.pos):
            self.print()
            print("BLACK WINS!!")
        else:
            self.print()
            print("DRAW!! OR GAME OVER!!")
    
    def single_player(self):
        player = 0
        #tree = self.build_tree("R")
        while(not(self.check_win("R", self.pos)) and not(self.check_win("B", self.pos)) and not(self.board_full())):
            self.print()
            if player == 0:
                move = input("Player Move: ")
            elif player == 1:
                move = self.tree_best_move(self.pos)
                #move = self.random_player()
            if move == "h":
                self.print_help()
            elif move == "exit":
                exit()
            elif move == "next":
                self.suggest_move(self.pos)
            elif move == "b":
                if self.is_empty():
                    print("Board is empty, please make a move first.\n")
                else:
                    self.remove_move()
            elif move == "s":
                print(self.check_score("R",self.pos))
            else:
                if move not in ['1','2','3','4','5','6','7']:
                    self.print_help()
                    move = input("not a valid move try again: ")
                if player == 0:
                    while(self.move(int(move)-1, 'R')):
                        move = input("Player One Move Again(Invalid Position): ")
                    player = 1
                elif player == 1:
                    while(self.move(int(move)-1, 'B')):
                        move = input("Player Two Move Again(Invalid Position): ")
                    player = 0
        if self.check_win("R", self.pos):
            self.print()
            print("RED WINS!!")
        elif self.check_win("B", self.pos):
            self.print()
            print("BLACK WINS!!")
        else:
            self.print()
            print("DRAW!! OR GAME OVER!!")
board = Game_board()
board.single_player()
