from __future__ import annotations
import re

class Node:
    
    def __init__(self, value, weight: int):
        self.parent: Node | None = None
        self.leftChild: Node | None = None
        self.rightChild: Node | None = None
        self.value = value
        self.weight = weight
        self.coeff: int = 0
        self.bf: int = 0
        
    def __eq__(self, node: "Node"):
        return self.weight == node.weight
        
    def __gt__(self, node: "Node"):
        return self.weight > node.weight
    
    def __lt__(self, node: "Node"):
        return self.weight < node.weight
    
    def __ge__(self, node: "Node"):
        return self.weight >= node.weight
    
    def __le__(self, node: "Node"):
        return self.weight <= node.weight
    
    @property
    def parent(self) -> Node | None:
        return self._parent
    
    @parent.setter
    def parent(self, node: "Node"):
        self._parent = node
        
    @property
    def leftChild(self) -> Node | None:
        return self._leftChild
    
    @leftChild.setter
    def leftChild(self, node: "Node"):
        self._leftChild = node
        
    @property
    def rightChild(self) -> Node | None:
        return self._rightChild
        
    @rightChild.setter
    def rightChild(self, node: "Node"):
        self._rightChild = node
        
    @property
    def weight(self) -> int:
        return self._weight
        
    @weight.setter
    def weight(self, number: "int"):
        self._weight = number
        
    @property
    def bf(self) -> int:
        return self._bf
    
    @bf.setter
    def bf(self, number: "int"):
        self._bf = number
        
    @property
    def coeff(self) -> int:
        return self._coeff
        
    @coeff.setter
    def coeff(self, number: "int"):
        self._coeff = number
        
        
class ExpressionTree:
    
    def __init__(self):
        self.root: Node | None = None
        self.current: Node| None = None
        self.nodes = {}
        
    @staticmethod
    def height(node: "Node") -> int:
        if node is None:
            return 0
        return 1 + max(ExpressionTree.height(node.leftChild), ExpressionTree.height(node.rightChild))
    
    @staticmethod
    def updateBalance(node: "Node"):
        if node is None:
            return
        node.bf = ExpressionTree.height(node.leftChild) - ExpressionTree.height(node.rightChild)
        ExpressionTree.updateBalance(node.leftChild)
        ExpressionTree.updateBalance(node.rightChild)
    
    @staticmethod
    def left_rotate(x: "Node", y: "Node"):
        temp = y.leftChild
        y.leftChild = x
        y.parent = x.parent
        if x.parent is not None:
            if x.parent.leftChild is x:
                x.parent.leftChild = y
            else:
                x.parent.rightChild = y
        x.parent = y
        x.rightChild = temp
        if temp is not None: 
            temp.parent = x
        
    @staticmethod
    def right_rotate(x: "Node", y: "Node"):
        temp = y.rightChild
        y.rightChild = x
        y.parent = x.parent
        if x.parent is not None:
            if x.parent.leftChild is x:
                x.parent.leftChild = y
            else:
                x.parent.rightChild = y
        x.parent = y
        x.rightChild = temp
        if temp is not None: 
            temp.parent = x
        
    @staticmethod
    def insert(root: "Node", node: "Node") -> Node | None:
        if root is None:
            return node
        if root > node:
            if root.leftChild is None:
                root.leftChild = node
                node.parent = root
                return root
            else:
                root.leftChild = ExpressionTree.insert(root.leftChild, node)
                return root
        if root <= node:
            if root.rightChild is None:
                root.rightChild = node
                node.parent = root
                return root
            else:
                root.rightChild = ExpressionTree.insert(root.rightChild, node)
                return root
        return None
    
    def balance(self):
        def balance_node(node: Node | None):
            if node is None:
                return
            if node.bf > 1:
                if node.leftChild is not None and node.leftChild.bf >= 1:
                    ExpressionTree.right_rotate(node, node.leftChild)
                elif node.leftChild is not None and node.leftChild.bf <= -1:
                    ExpressionTree.left_rotate(node.leftChild, node.leftChild.rightChild)
                    ExpressionTree.right_rotate(node, node.leftChild)
            elif node.bf < -1:
                if node.rightChild is not None and node.rightChild.bf <= -1:
                    ExpressionTree.left_rotate(node, node.rightChild)
                elif node.rightChild is not None and node.rightChild.bf >= 1:
                    ExpressionTree.right_rotate(node.rightChild, node.rightChild.leftChild)
                    ExpressionTree.left_rotate(node, node.rightChild)
            balance_node(node.leftChild)
            balance_node(node.rightChild)
            ExpressionTree.updateBalance(node)
        balance_node(self.root)
    
    def append(self, op):
        if op == '+':
            self.root = ExpressionTree.infix(self.root, Node(op, 1))
        elif op == '-':
            self.root = ExpressionTree.infix(self.root, Node(op, 2))
        elif op == "*": 
            self.root = ExpressionTree.infix(self.root, Node(op, 3))
        elif op == "/":
            self.root = ExpressionTree.infix(self.root, Node(op, 4))
        elif op == "^":
            self.root = ExpressionTree.infix(self.root, Node(op, 5))
        elif op.isdigit():
            self.root = ExpressionTree.infix(self.root, Node(int(op), 6))
    
    @staticmethod
    def infix(root: "Node", node: "Node") -> "Node":
        if root is None:
            return node
        if root >= node:
            node.leftChild = root
            if root.weight == 6:
                root.parent = node
            else:
                root.parent = ExpressionTree.infix(root.parent, node)
            return node
        if root < node:
            node.parent = root
            root.rightChild = ExpressionTree.infix(root.rightChild, node)
            return root
        return None
    
    
    def evaluateExp(self) -> float:
        def evaluate(node: "Node") -> float:
            if node is None:
                return 0
            if node.weight == 1:
                return evaluate(node.leftChild) + evaluate(node.rightChild)
            elif node.weight == 2:
                return evaluate(node.leftChild) - evaluate(node.rightChild)
            elif node.weight == 3:
                return evaluate(node.leftChild) * evaluate(node.rightChild)
            elif node.weight == 4:
                return evaluate(node.leftChild) / evaluate(node.rightChild)
            else:
                return node.value
        return evaluate(self.root)
    
def precedence(op):
    if op == '+' or op == '-':
        return 1
    if op == '*' or op == '/':
        return 2
    if op == '^':
        return 3
    return 0

def evaluate_postfix(tokens) -> float:
    stack = []
    for token in tokens:
        if token.isdigit():
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
        if token.isdigit():
            output.append(token)
        elif token == '(':
            stack.append(token)
        elif token == ')':
            while stack and stack[-1] != '(':
                output.append(stack.pop())
            stack.pop()  # Remove '('
        else:  # operator
            while stack and precedence(stack[-1]) >= precedence(token):
                output.append(stack.pop())
            stack.append(token)
    while stack:
        output.append(stack.pop())
    return output

oc = input("Write out an expression: ")
tokens = re.findall(r'\d+|[+\-*/^()]', oc)
postfix_tokens = infix_to_postfix(tokens)
print(f"Answer = {evaluate_postfix(postfix_tokens)}")