from __future__ import annotations

class Node:
    
    def __init__(self, value: int | str, weight: int):
        self.parent: Node | None = None
        self.leftChild: Node | None = None
        self.rightChild: Node | None = None
        self.value = value
        self.weight = weight
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
        
        
class WeightedTree:
    
    def __init__(self):
        self.root: Node | None = None
        self.nodes = {} 
        
    @staticmethod
    def height(node: "Node") -> int:
        if node is None:
            return 0
        return 1 + max(WeightedTree.height(node.leftChild), WeightedTree.height(node.rightChild))
    
    @staticmethod
    def updateBalance(node: "Node"):
        if node is None:
            return
        node.bf = WeightedTree.height(node.leftChild) - WeightedTree.height(node.rightChild)
        WeightedTree.updateBalance(node.leftChild)
        WeightedTree.updateBalance(node.rightChild)
    
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
                root.leftChild = WeightedTree.insert(root.leftChild, node)
                return root
        if root <= node:
            if root.rightChild is None:
                root.rightChild = node
                node.parent = root
                return root
            else:
                root.rightChild = WeightedTree.insert(root.rightChild, node)
                return root
        return None
    
    def balance(self):
        def balance_node(node: Node | None):
            if node is None:
                return
            if node.bf > 1:
                if node.leftChild is not None and node.leftChild.bf >= 1:
                    WeightedTree.right_rotate(node, node.leftChild)
                elif node.leftChild is not None and node.leftChild.bf <= -1:
                    WeightedTree.left_rotate(node.leftChild, node.leftChild.rightChild)
                    WeightedTree.right_rotate(node, node.leftChild)
            elif node.bf < -1:
                if node.rightChild is not None and node.rightChild.bf <= -1:
                    WeightedTree.left_rotate(node, node.rightChild)
                elif node.rightChild is not None and node.rightChild.bf >= 1:
                    WeightedTree.right_rotate(node.rightChild, node.rightChild.leftChild)
                    WeightedTree.left_rotate(node, node.rightChild)
            balance_node(node.leftChild)
            balance_node(node.rightChild)
            WeightedTree.updateBalance(node)
        balance_node(self.root)
        
    def append(self, op):
        if op == '+' or op == '-':
            self.root = WeightedTree.insert(self.root, Node(op, 1))
        elif op == "*" or op == "/":
            self.root = WeightedTree.insert(self.root, Node(op, 2))
        elif op == "^":
            self.root = WeightedTree.insert(self.root, Node(op, 3))
        else:
            self.root = WeightedTree.insert(self.root, Node(op, 0))
        WeightedTree.updateBalance(self.root)
        self.balance()
        return
    
    def appendToExp(self, op):
        if op == '+' or op == '-':
            self.root = WeightedTree.infix(self.root, Node(op, 1))
        elif op == "*" or op == "/":
            self.root = WeightedTree.infix(self.root, Node(op, 2))
        elif op == "^":
            self.root = WeightedTree.infix(self.root, Node(op, 3))
        else:
            self.root = WeightedTree.infix(self.root, Node(op, 0))
        return
    
    @staticmethod
    def infix(root: "Node", node: "Node") -> "Node":
        if root is None:
            return node
        if root.parent is None and root.leftChild is None:
            root.parent = node
            node.leftChild = root
            node.parent = root.parent
            if root.parent is not None:
                root.parent.leftChild = node
            return node
        if root.leftChild is not None and root.rightChild is None:
            root.rightChild = node
            node.parent = root
            return root
        if (root.parent is None and root.rightChild is not None) and root >= node:
            root.parent = node
            node.leftChild = root
            node.parent = root.parent
            if root.parent is not None:
                root.parent.leftChild = node
            return node
        if (root.parent is None and root.rightChild is not None) and root < node:
            root.parent = node
            node.leftChild = root
            return WeightedTree.infix(root.rightChild)
        return None
    
    def pop(self) -> str | int | None:
        if self.root is None:
            return None
        def post_order_traversal(node: "Node") -> Node:
            if node.leftChild is not None:
                return post_order_traversal(node.leftChild)
            if node.rightChild is not None:
                return post_order_traversal(node.rightChild)
            return node
        temp = post_order_traversal(self.root)
        if temp.parent is not None:
            if temp.parent.leftChild is temp:
                temp.parent.leftChild = temp.rightChild
                if temp.rightChild is not None:
                    temp.rightChild.parent = temp.parent
            else:
                temp.parent.rightChild = temp.rightChild
                if temp.rightChild is not None:
                    temp.rightChild.parent = temp.parent
        else:
            self.root = temp.rightChild
            if temp.rightChild is not None:
                temp.rightChild.parent = None
        return temp.value
    
    def hasNext(self):
        return self.root is not None
    
loc = "1+1*8"
e = WeightedTree()
for s in loc:
    e.appendToExp(s)
while e.hasNext():
    print(e.pop)