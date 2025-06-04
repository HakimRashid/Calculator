from __future__ import annotations
import re       
        
            
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    if op == '^':
        return 3
    return 0

def is_number(value) -> bool:
    try:
        float(value)
        return True
    except ValueError:
        return False

def evaluate_postfix(tokens) -> float:
    stack = []
    for token in tokens:
        if is_number(token):
            stack.append(float(token))
        else:
            b = stack.pop()
            a = stack.pop()
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                stack.append(a / b)
            elif token == '^':
                stack.append(a ** b)
    return stack[0]
        
def infix_to_postfix(tokens):
    output = []
    stack = []
    for token in tokens:
        if is_number(token):
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()
        else:
            while stack and precedence(stack[-1]) >= precedence(token):
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return output

def evaluate_expression(text) -> float:
    tokens = re.findall(r'\d*\.\d+|\d+|[+\-*/^()]', text)
    postfix_tokens = infix_to_postfix(tokens)
    return evaluate_postfix(postfix_tokens)
    
def main():
    oc = input("Write out an expression: ")
    print(f"Answer = {evaluate_expression(oc)}")
        
if __name__ == '__main__':
    main()