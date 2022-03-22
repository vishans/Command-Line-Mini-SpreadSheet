
# from os import error
import numpy as np
from satck import Stack, Utility
import pandas as pd

parenthesis = { '{': '}',
                '[': ']',
                '(': ')' 
               }

operators = ['+', '-', '*', '/']

def expressionSyntaxCheck(exp: str) -> bool:

    index = 0
    pCount = 0
    
    variable = False 
    digit = False
    exp = exp.strip()

    len_exp = len(exp)

    if exp[0] in operators or exp[-1] in operators:
        return False


    while index < len_exp:

        if exp[index] == ' ':  #ignoring whitespace
            index+=1
            continue

        if exp[index] == '(': 
            pCount +=1
            temp_index = index
            temp_index +=1

            while exp[temp_index] == ' ': #ignoring any whitespaces after (
                temp_index +=1

            if exp[temp_index] in operators or exp[temp_index] == ')':  # if there's a ) or an operator after the (  then the expression is invalid
                return False

            else:
                index += 1 
                continue 


        if exp[index] == ')':
            pCount -=1
            temp_index = index
            temp_index -=1
            while exp[temp_index] == ' ':
                temp_index -=1

            if exp[temp_index] in operators or exp[temp_index] == '(':
                return False

            else:
                index += 1 
                continue 

        if 'A' <= exp[index] <= 'Z':
            if not variable and not digit:  #a variable can start only with one letter
                variable = True
                index +=1
                continue

            else:
                return False

        variable = False

        if '0' <= (exp[index]) <= '9' :
            digit = True
            index += 1

            continue
        

       

        if digit and exp[index] in operators:
            digit = False
            index +=1 

            continue
        

        return False

    if pCount != 0 or variable:
        return False
    
    
    return True

def replaceVariable(exp: str, grid):
    index = 0
    lock = False
    temp_var = ''
    temp_var_len = 0

    exp_len = len(exp)
    while index < exp_len:
        # print(f'index is {index} and c is {exp[index]} and len is {exp_len} but p says {len(exp)}')
        if exp[index] == ' ':  #ignoring whitespace
            index+=1
            continue


        if not lock and 'A' <= exp[index] <= 'Z':
            lock = True
            temp_var += exp[index]
            temp_var_len += 1
            index +=1 
            continue


        if lock:
            
            if exp[index] in operators or exp[index] == ')':
                
                # print('index at ' + exp[index] + ' before  and index is ' + str(index) + ' ml ' + str(exp_len) +'  pl ' + str(len(exp)))


                lock = False
                # print(temp_var + '  ' +  str(temp_var_len))

                gotten_val = getValueFromGrid(temp_var,grid)

                if gotten_val == 'Error':
                    return gotten_val

                gotten_val_len = len(gotten_val)
                surplus = gotten_val_len - temp_var_len
                exp = exp.replace(temp_var,gotten_val, 1)
                # print(exp + '  len  ' + str(len(exp)))
                index += surplus
                exp_len += surplus 
                # exp_len = len(exp)
                # print('index at ' + exp[index] + ' after  and index is ' + str(index) + ' ml ' + str(exp_len) +'  pl ' + str(len(exp)))

                # print()

                temp_var = ''
                temp_var_len = 0
                

            else:
                temp_var += exp[index]
                temp_var_len += 1


                if index == len(exp) - 1:
                    # pass
                    # print('index at ' + exp[index] + ' before and index is ' + index)
                    lock = False
                    # print(temp_var + '  ' +  str(temp_var_len))

                    gotten_val = getValueFromGrid(temp_var,grid)

                    if gotten_val == 'Error':
                        return gotten_val
                    
                    gotten_val_len = len(gotten_val)
                    surplus = gotten_val_len - temp_var_len
                    exp = exp.replace(temp_var,gotten_val,1)
                    # print(exp)
                    index += surplus
                    exp_len += surplus 
                    # print('index at ' + exp[index] + ' after  and index is ' + index)
                    # print()

                    break

                    

            # index+=1


        index += 1

    return exp

    '''Note the replace function can actually replace several occurrences of a variable for example
       exp = 'A1 + 69 + A1' the A1 at the begining would summon replace but the latter will also take care
       of A1 at the end. It's somewhat more efficient since it will limit function calls as the
       first occurence of any variable would replace other occurences on its own, all that by extracting
       value from the grid only once. But for this to work properly, exp_len = len(exp) instead  of 
       exp_len += surplus.Since several occurences of the same variable might be replaced, we can't rely on 
       the maths of adding surplace to get the actual length. We could do 
       sexp_len += surplus * number_of_occurences_changed but that would mean tracking the number of 
       occurences that were changed. The easier and most straight foward way out would just do
       exp_len = len(exp).

       This version is not implemented above.
       '''


def getValueFromGrid(cellAddress, grid):
    # print(cellAddress)
    col = ord(cellAddress[0]) - 65
    row = int(cellAddress[1:3]) - 1

    # print(row, col)

    if col < 0 or row < 0:

        return 'Error'

    try:

        return str(grid[row][col]) 

    except:

        return 'Error'


def parseExpression(exp, grid):
    try:
        return_val = 'Error'

        if expressionSyntaxCheck(exp):

            return_val = replaceVariable(exp, grid)

        if return_val != 'Error':
            f = InfixToPostfix(return_val)
            return_val =  evaluator(f)

        

        return return_val

    except:
        return 'Error'


def InfixToPostfix(exp):
    s = Stack()

    result = []
    index = 0 
    number = ''

    # otherThanNumber = False

    while index < len(exp):

        if exp[index] == ' ':
            index +=1
            continue

        if '0' <= exp[index] <= '9':

            number += exp[index]

            if index + 1 < len(exp):
                if not('0' <= exp[index+1] <= '9'):

                    result.append(number)
                    number =  ''

            else:

                result.append(number)

            index +=1
           
        else:


            if Utility.isAnOperator(exp[index]):

                while(not(s.isEmpty()) and Utility.hasHigherPrecedence(s.top(),exp[index]) and not(Utility.isOpenParenthesis(exp[index]))):

                    result.append(s.pop())


                s.push(exp[index])

            elif Utility.isOpenParenthesis(exp[index]):
                s.push(exp[index])


            else: 

                #gotta be a close parenthesis

                while(not(s.isEmpty()) and not(Utility.isOpenParenthesis(s.top()))):

                    result.append(s.pop())


                s.pop() # pop the open parenthesis 

            index+=1

    
    while(not(s.isEmpty())):
        result.append(s.pop())


    return result


add = lambda a, b: a+b
subtract = lambda a, b: a-b
multiply = lambda a, b: a*b
divide = lambda a, b: a/b

def popNevalWrapper(fn):
    
    def popNeval(stack):

        b = int(stack.pop())
        a = int(stack.pop())

        stack.append(fn(a,b))

    return popNeval


dispatch = {
    '+': popNevalWrapper(add),
    '-': popNevalWrapper(subtract),
    '*': popNevalWrapper(multiply),
    '/': popNevalWrapper(divide),

}



def evaluator(exp: list):

    stack = []
    

    for op in exp:

        if op in dispatch:

            dispatch[op](stack)

        else:

            stack.append(op)


    return (stack[0])





        
if __name__ == '__main__':

    

    print(InfixToPostfix('1-6'))
