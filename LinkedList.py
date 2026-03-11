import logging

logger = logging.getLogger(__name__)

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
            
            Attributes: 
            head (Node | None): The pointer of first entry of the LinkedList
            tail (Node | None): The pointer of the last entry of the LinkedList
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
                    
        except OSError as e:
            logger.error(f'Error opening data.db for LinkedList.set(): {e}')
            raise
    
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
