from random import shuffle

class Game_board:
    pos = []
    moves = []

    class Game_tree:
        board = []
        moves = []
        def __init__(self, board):
            self.board = board
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
    def check_win(self, symbol):
        for i in range(6):
            for j in range(7):
                if self.pos[i][j] == symbol:
                    if (j - 3) >= 0:
                        if (i + 3) <= 5: #5? maybe? check for off by one
                            #check stright up and diagonal up left
                            if self.pos[i+1][j] == symbol and self.pos[i+2][j] == symbol and self.pos[i+3][j] == symbol:
                                return True
                            if self.pos[i+1][j-1] == symbol and self.pos[i+2][j-2] == symbol and self.pos[i+3][j-3] == symbol:
                                return True   
                        #check left I dont think this is needed, we will just need to check right. but whatever.
                        if self.pos[i][j-1] == symbol and self.pos[i][j-2] == symbol and self.pos[i][j-3] == symbol:
                            return True
                    if (j + 3) <= 6: #6? maybe?
                        if(i + 3) <= 5:
                            #check up and up right
                            if self.pos[i+1][j] == symbol and self.pos[i+2][j] == symbol and self.pos[i+3][j] == symbol:
                                return True
                            if self.pos[i+1][j+1] == symbol and self.pos[i+2][j+2] == symbol and self.pos[i+3][j+3] == symbol:
                                return True
                        #check right
                        if self.pos[i][j+1] == symbol and self.pos[i][j+2] == symbol and self.pos[i][j+3] == symbol:
                            return True
        return False
    
    def check_score(self, symbol, first=0):
        if first == 0:
            other_score = self.check_score("B" if symbol == "R" else "R", 1)
        score = 0
        #counted = []
        for i in range(6):
            for j in range(7):
                up_checked = 0
                if self.pos[i][j] == symbol:
                    if (j - 3) >= 0:
                        if (i + 3) <= 5: #5? maybe? check for off by one
                            #check stright up and diagonal up 
                            if self.pos[i+1][j] == symbol and self.pos[i+2][j] == symbol and self.pos[i+3][j] == '*' and up_checked == 0:
                                score += 50
                                up_checked = 1
                            elif self.pos[i+1][j] == symbol and self.pos[i+2][j] == '*' and up_checked == 0:
                                if i > 0:
                                    if self.pos[i-1][j] == symbol:
                                        pass
                                    else:
                                        score += 10
                                        up_checked = 1
                                else:
                                    score += 10
                                    up_checked = 1
                            if self.pos[i+1][j-1] == symbol and self.pos[i+2][j-2] == symbol and self.pos[i+3][j-3] == '*':
                                score += 50   
                            elif self.pos[i+1][j-1] == symbol and self.pos[i+2][j-2] == '*':
                                score += 10
                    if (j + 3) <= 6: #6? maybe?
                        if(i + 3) <= 5:
                            #check up and up right (need to figure out how not to double add up)
                            if self.pos[i+1][j] == symbol and self.pos[i+2][j] == symbol and self.pos[i+3][j] == '*' and up_checked == 0:
                                score += 50
                                up_checked = 1
                            elif self.pos[i+1][j] == symbol and self.pos[i+2][j] == '*' and up_checked == 0:
                                if i > 0:
                                    if self.pos[i-1][j] == symbol:
                                        pass
                                    else:
                                        score += 10
                                        up_checked = 1
                                else:
                                    score += 10
                                    up_checked = 1

                            #up right
                            if self.pos[i+1][j+1] == symbol and self.pos[i+2][j+2] == symbol and self.pos[i+3][j+3] == '*':
                                score += 50
                            elif self.pos[i+1][j+1] == symbol and self.pos[i+2][j+2] == '*':
                                score += 10
                        #check right
                        if self.pos[i][j+1] == symbol and self.pos[i][j+2] == symbol and self.pos[i][j+3] == '*':
                            score += 50
        if first == 1:
            return score
        else:
            return score - other_score

    def print_help(self):
        print("'h' for help")
        print("Red goes first player enters 1-7 to pick which slot to play in")
        print("b to go back a move")
        print("exit to exit")

    def random_player(self):
        moves = [1,2,3,4,5,6,7]
        shuffle(moves)
        print(moves)
        return str(moves.pop())

    def two_play_game(self):
        player = 0
        while(not(self.check_win("R")) and not(self.check_win("B")) and not(self.board_full())):
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
                print(self.check_score("R"))
            else:
                if player == 0:
                    while(self.move(int(move)-1, 'R')):
                        move = input("Player One Move Again(Invalid Position): ")
                    player = 1
                elif player == 1:
                    while(self.move(int(move)-1, 'B')):
                        move = input("Player Two Move Again(Invalid Position): ")
                    player = 0
        if self.check_win("R"):
            self.print()
            print("RED WINS!!")
        elif self.check_win("B"):
            self.print()
            print("BLACK WINS!!")
        else:
            self.print()
            print("DRAW!! OR GAME OVER!!")
    
    def single_player(self):
        player = 0
        while(not(self.check_win("R")) and not(self.check_win("B")) and not(self.board_full())):
            self.print()
            if player == 0:
                move = input("Player Move: ")
            elif player == 1:
                move = self.random_player()
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
                print(self.check_score("R"))
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
        if self.check_win("R"):
            self.print()
            print("RED WINS!!")
        elif self.check_win("B"):
            self.print()
            print("BLACK WINS!!")
        else:
            self.print()
            print("DRAW!! OR GAME OVER!!")
board = Game_board()
board.single_player()
