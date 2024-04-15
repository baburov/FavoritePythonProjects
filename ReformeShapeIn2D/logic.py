from complex_shape import *

class Stack():
    def __init__(self, head):
        self.stack = []
        self.stack.append(head)
    def push(self, element):
        self.stack.append(element)
    def pop(self):
        self.stack.pop()
    def get(self):
        return self.stack[-1]