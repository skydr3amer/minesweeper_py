from enum import Enum, auto
import random

class GridStatus(Enum):
    bomb = 1
    hint = 2

class PlayerAction(Enum):
    unclicked = 1
    clicked = 2
    flag = 3

class Grid:
    def __init__(self,x,y):
        self.x_position = x
        self.y_position = y
        self.status = GridStatus.hint
        self.hint_counter = 0
        self.action = PlayerAction.unclicked
        
class Game:
    def create_boad(self, level):
        self.level = level
        self.board = [[Grid(r,c) for r in range(level)] for c in range(level)]
    
    def place_bombs(self):
        self.bombs_position = []
        bombs_plante = 0
        while bombs_plante < self.level:
            r = random.choice(range(0,self.level))
            c = random.choice(range(0,self.level))
            if ([r,c] in self.bombs_position) or ([r,c] == [self.first_click_r, self.first_click_c]):
                pass
            else:
                self.bombs_position.append([r,c])
                self.board[r][c].status = GridStatus.bomb
                self.board[r][c].hint_counter = "x"
                bombs_plante += 1
                
    def place_hints(self):
        for bomb in self.bombs_position:
            row = bomb[0]
            col = bomb[1]
            for r in range(max(0, row - 1), min((self.level - 1), (row + 1))+1):
                for c in range(max(0, col - 1), min((self.level - 1), (col + 1))+1):
                    if (self.board[r][c].status == GridStatus.hint):
                        self.board[r][c].hint_counter += 1
                        self.board[r][c].status = GridStatus.hint

    def checkClickedGrid(self,row,col):
        if self.board[row][col].action == PlayerAction.clicked:
            return
        
        if (self.board[row][col].hint_counter != 0):
            self.board[row][col].action = PlayerAction.clicked
            return

        # case when its 0
        self.board[row][col].action = PlayerAction.clicked
        for r in range(max(0, row - 1), min((self.level - 1), (row + 1))+1):
            for c in range(max(0, col - 1), min((self.level - 1), (col + 1))+1):
                if (r==row) and (c==col):
                    continue
                self.checkClickedGrid(r,c)
        

    def consol_view(self, reveal_all = False):
        visible_board = [[None for _ in range(self.level)] for _ in range(self.level)]
        for row in range(self.level):
            for col in range(self.level):
                if reveal_all == True:
                    visible_board[row][col] = str(self.board[row][col].hint_counter)
                else:
                    if self.board[row][col].action == PlayerAction.clicked:
                        visible_board[row][col] = str(self.board[row][col].hint_counter)
                    else:
                        visible_board[row][col] = ' '
        
        #copied to make it pretty
        
        # put this together in a string
        string_rep = ''
        # get max column widths for printing
        widths = []
        for idx in range(self.level):
            columns = map(lambda x: x[idx], visible_board)
            widths.append(
                len(
                    max(columns, key = len)
                )
            )

        # print the csv strings
        indices = [i for i in range(self.level)]
        indices_row = '   '
        cells = []
        for idx, col in enumerate(indices):
            format = '%-' + str(widths[idx]) + "s"
            cells.append(format % (col))
        indices_row += '  '.join(cells)
        indices_row += '  \n'
        
        for i in range(len(visible_board)):
            row = visible_board[i]
            string_rep += f'{i} |'
            cells = []
            for idx, col in enumerate(row):
                format = '%-' + str(widths[idx]) + "s"
                cells.append(format % (col))
            string_rep += ' |'.join(cells)
            string_rep += ' |\n'

        str_len = int(len(string_rep) / self.level)
        string_rep = indices_row + '-'*str_len + '\n' + string_rep + '-'*str_len

        return string_rep

def play():
    game = Game()
    level = int(input("Input a level: "))
    game.create_boad(level)
    game.first_click_r, game.first_click_c = [int(x) for x in input("Take a guess to start the game? Input as row,col: ").split(",")]
    game.board[game.first_click_r][game.first_click_c].action = PlayerAction.clicked
    game.place_bombs()
    game.place_hints()
    print(game.consol_view(True))

    nclick = 1
    safe = True
    while nclick <= ((level ** 2) - level):
        row, col =  [int(x) for x in input("Where would you like to guess? Input as row,col: ").split(",")]
       
        if row < 0 or row > level  or col < 0 or col > level:
            print("Invalid location. Try again.")
            continue    

        if (game.board[row][col].status == GridStatus.bomb):
            safe = False
            break
        else:
            if game.board[row][col].action == PlayerAction.clicked:
                continue
            else:
                game.checkClickedGrid(row,col)
                print(game.consol_view())
                nclick += 1

    if safe:
         print(f"CONGRATULATIONS!!!! YOU FOUND ALL THE {level} BOMBS!")
    else:
        print("SORRY GAME OVER :(")
        print(game.consol_view(True))

if __name__ == '__main__':
    play()
