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
    
    def set(self, key, value, persist=True):
        try:
            # Check if the key exists in the logs 
            current = self.head
            while current:
                if current.key == key:
                    current.value = value
                    if persist:
                        with open('data.db', 'a') as f:
                            f.write(f"{key},{value}\n")
                    return
                current = current.next

            # If the node doesn't exist, create new node and add to the list, and append as normal
            new_node = Node(key, value)

            if self.head is None:
                self.head = new_node
                self.tail = new_node

            else:
                self.tail.next = new_node
                self.tail = new_node

            if persist:
                with open('data.db', 'a') as f:
                    line = f"{new_node.key},{new_node.value}\n"
                    f.write(line)

        except IOError as e:
            print(f"Error appending to data.db: {e}")
    
    def get(self, key):
        current = self.head
        result = None

        while current:
            if current.key == key:
                print(current.value)
                return
            current = current.next
        return

def load_from_disk():
    key_vals = LinkedList()

    if os.path.exists('data.db'):
        with open('data.db', 'r') as f:
            for line in f:
                line = line.strip()
                if line:
                    key, value = line.split(',', 1)
                    key_vals.set(key, value, persist=False)
    return key_vals
             

def main(): 
    key_vals = load_from_disk()

    while (True):
        user_input = input()
        command = user_input.split()[0]
        match command:
            case 'SET':
                parts = user_input.split()
                key = parts[1]
                value = parts[2]
                key_vals.set(key, value)
            case 'GET':
                parts = user_input.split()
                key = parts[1]
                key_vals.get(key)
            case 'EXIT':
                break

    
    return 0




if __name__ == '__main__':
    main()