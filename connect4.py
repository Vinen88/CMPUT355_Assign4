class Game_board:
    pos = []
    moves = []
    def __init__(self):
        self.pos = [["*" for i in range(7)] for i in range(6)]
    def print(self):
        for row in reversed(self.pos):
            for position in row:
                print(position, end='\t')
            print('\n')
        print("1\t2\t3\t4\t5\t6\t7")
    def move(self, position, player):
        for row in self.pos:
            if row[position] == "*":
                row[position] = player
                return False
        return True
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

    def print_help(self):
        print("'h' for help")
        print("Red goes first player enters 1-7 to pick which slot to play in")
        print("B to go back a move")
        print("exit to exit")

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
                pass # need to do this still lolololol
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
board = Game_board()
board.two_play_game()
