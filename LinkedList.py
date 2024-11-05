from __future__ import print_function
class node:
    def __init__(self, data):
        self.data = data
        self.next = None

class LinkedList:
    def __init__(self):
        self.head = None

    def traversal(self):
        if self.head is None:
            print("It is empty")
        else:
            a = self.head
            while a is not None:
                print(a.data, end=' ')
                a = a.next

ll = LinkedList()
n1 = node(1)
ll.head = n1
n2 = node(3)
n1.next = n2
n3 = node(5)
n2.next = n3
n4 = node(10)
n3.next = n4
ll.traversal()