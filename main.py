import os

class Node:
    '''
        Represents a single entry in the key-value store as a node in a singly linked list.
        Each node holds one key-value pair and a reference to the next node.

        Attributes:
            key (str): The unique identifier used to look up this entry.
            value (str): The data associated with the key.
            next (Node | None): Pointer to the next node in the list; None if this is the tail.
    '''
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


class LinkedList:
    def __init__(self):
        '''
            Initializes an empty linked list by setting both head and tail to None.
            head points to the first node for traversal;
            tail points to the last node for O(1) appends.
        '''
        self.head = None
        self.tail = None
    
    def set(self, key, value, persist=True):
        '''
            Inserts a new key-value pair or updates the value of an existing key.
            Traverses the list to check for a duplicate key first; if found, the
            existing node's value is updated in-place. If no match is found, a new
            node is appended to the tail for O(1) insertion.

            When persist=True (the default), the operation is also written to data.db
            so it survives restarts. persist=False is used during startup when
            replaying data.db to avoid writing entries that already exist on disk.

            Args:
                key (str): The unique identifier for this entry.
                value (str): The data to store under the given key.
                persist (bool): Whether to append this write to data.db. Default True.

            Raises:
                Exception: If the data.db file cannot be opened for writing.
        '''
        try:
            # Walk the list looking for an existing node with this key.
            # If found, overwrite its value in memory and log the update to disk.
            current = self.head
            while current:
                if current.key == key:
                    current.value = value
                    if persist:
                        with open('data.db', 'a') as f:
                            f.write(f"{key},{value}\n")
                    return
                current = current.next

            # Key not found — allocate a new node and append it to the tail of the list.
            new_node = Node(key, value)

            if self.head is None:
                self.head = new_node
                self.tail = new_node

            else:
                self.tail.next = new_node
                self.tail = new_node

            # Only write to disk when persist=True; skipped during the initial
            # load_from_disk() replay to avoid duplicating entries already on disk.
            if persist:
                with open('data.db', 'a') as f:
                    f.write(f"{new_node.key},{new_node.value}\n")
                    
        except IOError as e:
            raise Exception(f'Error opening file: {e}')
    
    def get(self, key):
        '''
            Retrieves the value associated with the given key by performing a linear
            scan of the linked list from head to tail. Returns None if the key is
            not present. Time complexity is O(n) where n is the number of stored entries.

            Args:
                key (str): The identifier to search for.

            Returns:
                str | None: The stored value if the key exists, otherwise None.
        '''
        current = self.head

        # Traverse each node; return immediately on a key match, or None if exhausted.
        while current:
            if current.key == key:
                return current.value
            current = current.next
        return None

def load_from_disk():
    '''
        Reconstructs the in-memory linked list by replaying the data.db log file.
        Each line in data.db is expected to be in "key,value" format. Lines that
        do not conform (missing the comma separator or extra/missing fields) are
        skipped with a warning so a single corrupt entry doesn't prevent startup.

        persist=False is passed to LinkedList.set() during replay to avoid
        re-writing entries that are already persisted on disk.

        Returns:
            LinkedList: The fully populated key-value store ready for use.

        Raises:
            Exception: If data.db exists but cannot be opened for reading.
    '''
    try:
        key_vals = LinkedList()

        if os.path.exists('data.db'):
                with open('data.db', 'r') as f:
                        for line in f:
                                line = line.strip()
                                if line:
                                        parts = line.split(',', 1)
                                        if len(parts) != 2:
                                                print(f"Skipping malformed line in data.db: {repr(line)}")
                                                continue
                                        key, value = parts
                                        key_vals.set(key, value, persist=False)
        return key_vals
    except IOError as e:
         raise Exception(f'Error loading from disk: {e}')
             

def main():
    '''
        Entry point for the key-value store CLI.
        Restores any previously persisted data via load_from_disk(), then enters
        an interactive read-eval loop that accepts three commands from stdin:

            SET <key> <value>  — Store or overwrite the value for the given key.
            GET <key>          — Print the value for the given key (no output if missing).
            EXIT               — Flush any pending output and terminate the process.

        Returns:
            int: Exit code 0 on clean shutdown.
    '''
    key_vals = load_from_disk()

    while True:
        try:
            user_input = input().strip()
        except EOFError:
            # stdin pipe closed
            break

        if not user_input:
            # Skip blank lines instead of crashing
            continue

        parts = user_input.split(maxsplit=2)
        command = user_input.split()[0]

        match command:
            case 'SET':
                # Split into at most 3 parts so values containing spaces are preserved.
                key = parts[1]
                value = parts[2]
                key_vals.set(key, value)
            case 'GET':
                key = parts[1]
                val = key_vals.get(key)
                # flush=True ensures the output is sent immediately
                if val:
                    print(val, flush=True)
            case 'EXIT':
                # Clean exit — break out of the loop and let main() return 0.
                break

    
    return 0




if __name__ == '__main__':
    main()