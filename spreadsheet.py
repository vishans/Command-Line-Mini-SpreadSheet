import os
import time 
import string
import threading
import msvcrt
from parser_ import parseExpression

clear = lambda: os.system('cls')



class SpreadSheet:
    SPACES = '    '
    CELL_LIMIT = 4+5
    CELL_FONT_COLOR = 90 #ANSI escape code for darkish color
    HIGHLIGHT_COLOR = 107 #white highlight
    CELL_WIDTH = 5+5
    SPACE_BTW_COL = 3

    ROW = 5
    COLUMN = 5

    def __init__(self) -> None:

        self.grid = [[None for _ in range(SpreadSheet.COLUMN)] for __ in range(SpreadSheet.ROW)]

        self.documentTitle = 'New Document'

        self.currentCell = [0,0]
        self.arrowThread = threading.Thread(target=self.listenAndMove)
        self.arrowActive = True
        self.commandPrompt = False
        self.arrowThread.start()

        self.title_formatlen = (SpreadSheet.CELL_WIDTH + SpreadSheet.SPACE_BTW_COL) * SpreadSheet.COLUMN
        self.error = False



    def show(self):

        clear()

        


        print(('\033[42m'+'{: ^'+ str(self.title_formatlen) +'s}').format('Spreadsheet - ' + self.documentTitle)+'\033[0m')

        if self.error:
            self.arrowActive = False


        
        space = ' ' * SpreadSheet.SPACE_BTW_COL
        for i in range(SpreadSheet.COLUMN):
            print(((space + '{: ^'+str(SpreadSheet.CELL_WIDTH)+'s}').format(string.ascii_uppercase[i])),end='')

        print()



        for  i in range(SpreadSheet.ROW):
            print((('{: ^'+str(SpreadSheet.SPACE_BTW_COL)+'s}').format(str(i+1))),end='')
            for j in range(SpreadSheet.COLUMN):
                content = self.grid[i][j]
                if [i,j] == self.currentCell:
                    highlight = SpreadSheet.HIGHLIGHT_COLOR
                else:
                    highlight = 0 


                if content == None:
                    formatted_text =('{: ^'+ str(SpreadSheet.CELL_WIDTH)+'s}').format('None')
                    # print(f"\033[{highlight};90m{formatted_text}\033[0m", end=' ')

                elif len(content) <= SpreadSheet.CELL_LIMIT:
                    formatted_text =('{: ^'+ str(SpreadSheet.CELL_WIDTH)+'s}').format(str(content))

                    # print(f"\033[{highlight};90m{formatted_text}\033[0m", end=' ')

                else:
                    formatted_text =('{: ^'+ str(SpreadSheet.CELL_WIDTH)+'s}').format(str(content[:3]+'..'))


                print(f"\033[{highlight};90m{formatted_text}\033[0m", end=(' '* SpreadSheet.SPACE_BTW_COL))

            print()

        


        # print(self.currentCell, end='')

        self.showActiveCell()
        i,j = self.currentCell
        print('\t\t' + str(self.grid[i][j]))
        

        if self.error:
            print(('\033[41m'+'{: ^'+ str(self.title_formatlen) +'s}').format('ERROR')+'\033[0m')


            time.sleep(1)
            self.arrowActive = True
            self.error = False
            self.show()


    def put(self,content: str, index: list):
        i,j = index

        self.grid[i-1][j-1] = content


    def changeCurrentCell(self, index: list):
        
        self.currentCell = index


    def listenAndMove(self):
        '''
        to navigate you can use
        arrow keys
        8 6 2 4 on the numpad(intended)
        or using wdsa like a gamer but it won't work if you have caps lock on(intended)
        '''
        one = False
        while True:
            if msvcrt.kbhit():
                key = msvcrt.getch()
                # print(key)  

                if key == b'\r':
                    self.arrowActive = False
                    self.commandPrompt = True



                if self.arrowActive and not self.commandPrompt:
                    if key == b'\x00':
                        one = True

                    if one and key != b'\x00' or key in [b'6',b'4',b'2',b'8', b'a',b's',b'w',b'd']:
                        one = False
                        
                        if key == b'M' or key == b'6' or key == b'd':
                            # print('right')
                            if 0 <= self.currentCell[1] < SpreadSheet.COLUMN - 1:
                                self.currentCell[1] += 1

                            else:
                                self.currentCell[1] = 0

                            self.show()
                            # print(self.currentCell)



                        elif key == b'P' or key == b'2'or key == b's':
                            # print('down')
                            if 0 <= self.currentCell[0] < SpreadSheet.ROW - 1:
                                self.currentCell[0] += 1

                            else:
                                self.currentCell[0] = 0

                            self.show()
                            # print(self.currentCell)

                        elif key == b'K' or key == b'4'or key == b'a':
                            # print('left')
                            if 0 < self.currentCell[1] <= SpreadSheet.COLUMN - 1:
                                self.currentCell[1] -= 1

                            else:
                                self.currentCell[1] = SpreadSheet.COLUMN - 1
                                
                            self.show()
                            # print(self.currentCell)

                        elif key == b'H' or key == b'8'or key == b'w':
                            # print('up')
                            if 0 < self.currentCell[0] <= SpreadSheet.ROW - 1:
                                self.currentCell[0] -= 1

                            else:
                                self.currentCell[0] = SpreadSheet.ROW - 1
                                
                            self.show()
                            

                        # self.show() could've been there. La flemme.

            # time.sleep(0.5)
        




    def cmdPrompt(self):

        while self.arrowActive:
            pass

        if self.commandPrompt:

            command = input('enter value: ')

            if command == '':
                pass

            elif command.lstrip()[0] == '=':
                i,j = self.currentCell
                self.grid[i][j] = str(parseExpression(command.lstrip()[1:].upper(), self.grid))
            
            elif command.strip()[0] == '$':

                if command.strip()[1:8] == 'RENAME(' and command.strip()[-1] == ')':
                    self.documentTitle = command.strip()[8:-1] if len(command.strip()[8:-1]) <21 else command.strip()[8:-1][:15] + '...'

                else:
                    self.error = True
            
            
            
            else:
                i,j = self.currentCell
                self.grid[i][j] = command


            self.arrowActive = True
            self.commandPrompt = False

            self.show()


    def showActiveCell(self):
        i,j = self.currentCell

        col = string.ascii_uppercase[j]
        row = str(i+1)

        print('\t' + col+row, end='')          

                






