import os
import json

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
        try:
            new_node = Node(key, value)
            if self.head is None:
                self.head = new_node
                self.tail = new_node

            else:
                self.tail.next = new_node
                self.tail = new_node

            with open('data.db', 'a') as f:
                line = f"{new_node.key},{new_node.value}"
                f.write(line)
            
            return

        except IOError as e:
            print(f"Error appending to data.db: {e}")
    
    def get(self, key):
        current = self.head
        while current:
            if current.key == key:
                print(current.key, current.value, '\n')
                return
            current = current.next
            
        
        print(f"{key} not found.")
        return
             

def main(): 
    key_vals = LinkedList()

    while (True):
        user_input = input()
        command = user_input.split()[0]
        print(command)
        match command:
            case 'SET':
                parts = user_input.split()
                print(parts)
                key = parts[1]
                value = parts[2]
                key_vals.set(key, value)
            case 'GET':
                parts = user_input.split()
                key = int(parts[1])
                key_vals.get(key)
            case 'EXIT':
                break

    
    return 0




if __name__ == '__main__':
    main()