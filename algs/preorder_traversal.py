class Node():
    def __init__(self,left,right,info):
        self.left = left
        self.right = right
        self.info = info

def preOrder(root, visited=[]):
    if root is not None:
        visited.append(root.info)
        if root.left:
            preOrder(root.left, visisted)
        if root.right:
            preOrder(root.right, visisted)

four = Node(None, None, 4)
three = Node(None, four, 3)
six = Node(None, None, 6)
five = Node(three, six, 5)
two = Node(None, five, 2)
root = Node(None, two, 1)
visisted = []
preOrder(root, visisted)
print(' '.join(map(str, visisted)))
