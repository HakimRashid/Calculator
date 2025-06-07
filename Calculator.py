from __future__ import annotations
import math
import re       


def precedence(op):
    if op in ('sin', 'cos', 'tan', 'sinh', 'cosh', 'tanh', 'arcsin', 'arccos', 'arctan', 'arcsinh', 'arccosh', 'arctanh', 'log', 'ln', 'sqrt', 'cbrt', 'exp', 'abs'):
        return 4 
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

def evaluate_postfix(tokens, deg: "bool") -> float:
    stack = []
    for token in tokens:
        if is_number(token):
            stack.append(float(token))
        else:
            b = stack.pop()
            if token in ('+', '-', '/', '*', '*', 'mod'):
                if len(stack) == 0:
                    a = 0
                else:
                    a = stack.pop()
            
            #binary mathematical functions
            if token == '+':
                stack.append(a + b)
            elif token == '-':
                stack.append(a - b)
            elif token == '*':
                stack.append(a * b)
            elif token == '/':
                if b == 0:
                    stack.clear()
                    stack.append("Undefined - " + str(a) + "/" + str(b))
                    return
                stack.append(a / b)
            elif token == '^':
                stack.append(a ** b)
            elif token == 'mod':
                stack.append(math.fmod(b, a))
            
            #unary mathematical functions
            elif token == '%':
                stack.append(b / 100)
            elif token == '!':
                if b < 0:
                    stack.clear()
                    stack.append("Undefined - " + str(b) + "!")
                stack.append(math.factorial(math.floor(b)))
            elif token == 'sqrt':
                if b < 0:
                    stack.clear()
                    stack.append("Undefined - sqrt("  + str(b) + ")")
                    return stack[0]
                stack.append(math.sqrt(b))
            elif token == 'cbrt':
                stack.append(math.cbrt(b))
            elif token == 'exp':
                stack.append(math.exp(b))
            elif token == 'abs':
                stack.append(math.fabs(b))
            elif token.startswith('log'):
                if b < 0:
                    stack.clear()
                    stack.append("Undefined - " + token + '('  + str(b) + ")")
                    return stack[0]
                base = float(token.replace('log', ''))
                if base <= 0:
                    stack.clear()
                    stack.append("Undefined - " + token)
                    return stack[0]
                stack.append(math.log(b, base))
            elif token == 'ln':
                if b <= 0:
                    stack.clear()
                    stack.append("Undefined - ln("  + str(b) + ")")
                    return stack[0]
                stack.append(math.log(b))
            elif token == 'sin':
                if deg:
                    stack.append(math.sin(math.radians(b)))
                else:
                    stack.append(math.sin(b))
            elif token == 'cos':
                if deg:
                    stack.append(math.cos(math.radians(b)))
                else:
                    stack.append(math.cos(b))
            elif token == 'tan':
                k = round(b / (math.pi / 2))
                if abs(b - k * (math.pi / 2)) < 1e-10 and k % 2 == 1:
                    stack.clear()
                    stack.append("Undefined - tan("  + str(b) + ")")
                    return stack[0]
                if deg:
                    stack.append(math.tan(math.radians(b)))
                else:
                    stack.append(math.tan(b))
            elif token == 'sinh':
                if deg:
                    stack.append(math.sinh(math.radians(b)))
                else:
                    stack.append(math.sinh(b))
            elif token == 'cosh':
                if deg:
                    stack.append(math.cosh(math.radians(b)))
                else:
                    stack.append(math.cosh(b))
            elif token == 'tanh':
                if deg:
                    stack.append(math.tanh(math.radians(b)))
                else:
                    stack.append(math.tanh(b))
            elif token == 'arcsin':
                if b > 1 or b < -1:
                    stack.clear()
                    stack.append("Undefined - arcsin("  + str(b) + ")")
                    return stack[0]
                if deg:
                    stack.append(math.asin(math.radians(b)))
                else:
                    stack.append(math.asin(b))
            elif token == 'arccos':
                if b > 1 or b < -1:
                    stack.clear()
                    stack.append("Undefined - arccos("  + str(b) + ")")
                    return stack[0]
                if deg:
                    stack.append(math.acos(math.radians(b)))
                else:
                    stack.append(math.acos(b))
            elif token == 'arctan':
                if deg:
                    stack.append(math.atan(math.radians(b)))
                else:
                    stack.append(math.atan(b))
            elif token == 'arcsinh':
                if deg:
                    stack.append(math.asinh(math.radians(b)))
                else:
                    stack.append(math.asinh(b))
            elif token == 'arccosh':
                if b < 1:
                    stack.clear()
                    stack.append("Undefined - arccosh("  + str(b) + ")")
                    return stack[0]
                if deg:
                    stack.append(math.acosh(math.radians(b)))
                else:
                    stack.append(math.acosh(b))
            elif token == 'arctanh':
                if b >= 1 or b <= -1:
                    stack.clear()
                    stack.append("Undefined - arctanh("  + str(b) + ")")
                    return stack[0]
                if deg:
                    stack.append(math.atanh(math.radians(b)))
                else:
                    stack.append(math.atanh(b))
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

def evaluate_expression(text, deg: "bool") -> float:
    text = text.replace('e', str(math.e))
    text = text.replace('pi', str(math.pi))
    text = text.replace('𝝿', str(math.pi))
    tokens = re.findall(r'\d*\.\d+|\d+|\w+|[+\-*/^()!%]', text)
    postfix_tokens = infix_to_postfix(tokens)
    return evaluate_postfix(postfix_tokens, deg)

def main():
    oc = input("Write out an expression: ")
    print(f"Answer = {evaluate_expression(oc, False)}")

if __name__ == '__main__':
    main()