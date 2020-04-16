import math
import operator
from collections import deque

#Global to define operator lookup
alg_operators = {
    '+':operator.add,
    '-':operator.sub,
    '*':operator.mul,
    '/':operator.truediv,
    '^':operator.pow
}

trig_operators = {
    'sin':math.sin,
    'tan':math.tan,
    'cos':math.cos
}
all_ops = ", ".join([key for key in {**alg_operators, **trig_operators}])

def main():
  
    #Print Instructions
    all_ops = ", ".join([key for key in {**alg_operators, **trig_operators}])
    print(f"\nThis caculator supports the following operators: {all_ops}")
    print("Note that any operand of a trigonometric functions will be turned into radians ")
    print("Please enter a space between each item")
    print("To run the prebuilt tests, input 'T'")
    print("To quit, simply input 'Q'\n\n")
        
    #Loop for multiple equations
    while True:
        
        #Input equation, check for quit, else return result
        equation = input('\nEnter an equation (type Q to quit): ').split(" ")
        if equation[0].upper() == "Q":
            break
        elif equation[0].upper() == "T":
            tests()
        elif "(" in equation:
            equation = parse_parentheses(equation)
            print(f"Result: {parentheses_equation(equation)}")
        else: 
            print(f"Result: {calculate(equation)}")


def calculate(equation):
    #Creating a stack and result var
    stack = deque([]) #Note the use of deque vs list as deque is more performant for left endpoint modifications
    result = 0

    #Adding in invisable multplys
    if len([x for x in equation if x in trig_operators.keys()]) > 0 and len(equation) % 2 !=0:
        equation.append("*")

    #Itterating through equation string
    for i in equation:
        #Appending numbers to stack
        if i.replace('.','').isnumeric():
            stack.appendleft(i)
        
        #Applying function on operator
        else:
            #Checking for imporper format
            if len(stack) < 2:
                print (f'Error: Insufficient values in expression: {equation}\n-Please check for proper postfix ordering!')
                break
            else:
                #Print stack for debugging
                # print (f'Stack: {stack}')
               
                #Handling Algebra Operators
                if i in alg_operators:
                    #Getting operands from stack (left right reversed)
                    n2 = float(stack.popleft())
                    n1 = float(stack.popleft())
                    #Using the proper function from the Algebra operators dic
                    result = alg_operators[i](n1,n2)
                    stack.appendleft(str(result))
               
                #Handling Trignometirc Operators
                else:
                    #Getting operands from stack
                    n1 = float(stack.popleft())
                    #Using the proper function from the Trigometric operators dic, converting operand to radians
                    result = trig_operators[i](n1)
                    stack.appendleft(str(result))
    
    #Returning result
    return result


def parentheses_equation(lst):
    #This function breaks the nest lists into computable operations using recursion
    try:
        while any(isinstance(x, list) for x in lst):
            if type(lst[0]) == list:
                lst[0] = parentheses_equation(lst[0])
            if type(lst[1]) == list:
                lst[1] = parentheses_equation(lst[1])
            if type(lst[2]) == list:
                result = str(calculate(lst[:2] + [lst[3]]))
                return [result] + lst[2]
        return str(calculate(lst))
    except IndexError:
        if len(lst) == 1: return str(lst[0])
        else: print (f'Error: Insufficient values in expression: {lst}\n-Please check for proper postfix ordering!')


def push(item, lst, depth):
    #Appends item into nested lists at given depth
    while depth:
        lst = lst[-1]
        depth -= 1

    lst.append(item)


def parse_parentheses(s):
    groups = []
    depth = 0
    #Splits a string with parenthesis into python lists
    s.insert(0, '(')
    s.append(')')
    try:
        for char in s:
            if char == '(':
                #Adding a nested list
                push([], groups, depth)
                depth += 1
            elif char == ')':
                depth -= 1
            else:
                push(char, groups, depth)
    #Error Handling
    except IndexError:
        raise ValueError('Parentheses mismatch')
    if depth > 0:
        raise ValueError('Parentheses mismatch')
    else:
        return groups


def tests():
    equations = [
        "( 3.141 ( 2 3 + ) ( 1.571 sin ) * ) 5 ^ )", 
        "10 2 8 * + 3 -", 
        "8 5 4 + * 7 -",
        "8 4 / 3 2 * 6 4 3 1 + * + - +",
        "3 4 2 * /",
        "( 3.141 ( 2 3 + ) ( 1.571 sin ) * ) 5 ^ ) ( 8 5 4 + * 7 - ) *"
    ]

    for equation in equations:
        print(f"Equation: {equation}")
        equation = equation.split(" ")
        if "(" in equation:
            equation = parse_parentheses(equation)
            print(f"Result: {parentheses_equation(equation)}")
        else: 
            print(f"Result: {calculate(equation)}")
        print()

if __name__ == '__main__':
    main()