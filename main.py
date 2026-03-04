import os

class Node:
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        self.head = None
        self.tail = None
    
    def set(self, key, value):
        pass
    
    def get(self):
        pass


def main(): 
    while (True):
        user_input = input()
        if user_input == 'EXIT':
            break
    
    return 0




if __name__ == '__main__':
    main()