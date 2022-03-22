from spreadsheet import SpreadSheet
from time import sleep

'''
NAVIGATION
Use arrow keys or AWSD or 4862 on the keypad to navigate

VALUE INPUT
To enter a value in a cell, go to the desired cell, press Enter and then finally input your value

CALCULATION/FORMULA
If you want to perform a calculation press enter on the desire cell, prepend yout calculation with an '='. For example =6+9 will get you 15 in the cell.

USING CELL VALUES IN CALCULATION
You can also use cell values in your calculations. If you had the value 5 in cell A1 and value
10 in cell B2. Performing =A1+B2 in cell C3 will give you value 15 in the latter.

IMPORTANT NOTE
The evalutor is simple and may have trouble with negative numbers. The expression parser was not built with that in mind. The expression =-1-6 will not work. In this example the postfix expression looks like this ['1', '6', '-', '-']. After evaluation 1 6 - which gives -5, it will try to to evaluate -5 (no operand) -
This won't work.

However =6-1 will work. 
This works, why? Take a look at its postfix epression: ['6', '1', '-'].
'''

myExcel = SpreadSheet()
myExcel.show() # show the speadsheet before entering the loop

while True:

    myExcel.cmdPrompt() # listens for input and responds accordingly
    sleep(.5) #refresh and sample rate = 2Hz