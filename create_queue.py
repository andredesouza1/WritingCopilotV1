from typing import List

class Paragraph:
    def __init__(self, paragraph:str):
        self.paragraph = paragraph
        self.bullet_points = []


class Node:
    def __init__(self, data):
        self.data = data
        self.next = None
        self.previous = None
       

class Queue:
    def __init__(self):
        self.head = None
        self.tail = None
        self.count = 0

    def enqueue(self, data):
        new_node = Node(data)
        if self.head is None:
            self.head = new_node
            self.tail = self.head
        else:
            new_node.previous = self.tail
            self.tail.next = new_node
            self.tail = new_node
        
        self.count += 1

    def dequeue(self):
        if self.count == 0:
            return None
        
        current = self.head
        if self.count == 1:
            self.count -= 1
            self.head = None
            self.tail = None
        elif self.count > 1:
            self.head = self.head.next
            self.head.previous = None
            self.count -= 1
        return current.data




