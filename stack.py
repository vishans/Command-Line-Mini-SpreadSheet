class Stack:


    def __init__(self) -> None:
        
        self.stack = []
        self.stackPointer = -1


    def isEmpty(self):

        return self.stackPointer == -1


    def pop(self):

        if self.isEmpty():
            return None


        value = self.stack.pop()

        self.stackPointer -= 1

        return value


    def push(self, value):

        self.stackPointer += 1 

        self.stack.append(value)


    def top(self):

        if self.isEmpty():
            return None


        return self.stack[self.stackPointer]


class Utility:

    precedence = ['/', '*', '+', '-']

    @staticmethod
    def hasHigherPrecedence(this, other):


        if this == '(':

            return False

        


        return Utility.precedence.index(this) < Utility.precedence.index(other)

    @staticmethod
    def isAnOperator(op):

        return op in Utility.precedence


    @staticmethod
    def isOpenParenthesis(c):

        return c in ['(']


    @staticmethod
    def isClosedParenthesis(c):

        return c in [')']



if __name__ == '__main__':
    print(Utility.isAnOperator(''))
    

