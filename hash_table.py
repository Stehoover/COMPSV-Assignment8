class Contact:
    '''
    Contact class to represent a contact with a name and number.
    Attributes:
        name (str): The name of the contact.
        number (str): The phone number of the contact.
    '''
    
    def __init__(self, name: str, number: str):
        self.name = name
        self.number = number
        
    def __str__(self) -> str:
        return f"{self.name}: {self.number}"

class Node:
    '''
    Node class to represent a single entry in the hash table's linked list.
    Attributes:
        key (str): The key (name) of the contact.
        value (Contact): The value (Contact object) associated with the key.
        next (Node or None): Pointer to the next node in case of a collision.
    '''
   
    def __init__(self, key: str, value: Contact):
        self.key = key
        self.value = value
        self.next = None

class HashTable:
    '''
    HashTable class to represent a hash table for storing contacts.
    Attributes:
        size (int): The size of the hash table (number of slots).
        data (list): The underlying array to store linked lists for collision handling.
    Methods:
        hash_function(key): Converts a string key into an array index.
        insert(key, number): Inserts a new contact or updates an existing one.
        search(key): Searches for a contact by name.
        print_table(): Prints the structure of the hash table.
    '''
    
    def __init__(self, size: int):
        self.size = size
        # Initialize the data array with `None` at each index
        self.data = [None] * self.size

    def hash_function(self, key: str) -> int:
        # Simple hash function: sum of ordinal values of characters in the key
        # and then take the modulus with the table size.
        hash_value = sum(ord(char) for char in key)
        return hash_value % self.size

    def insert(self, key: str, number: str) -> None:
        index = self.hash_function(key)
        new_contact = Contact(key, number)
        new_node = Node(key, new_contact)

        # Check if the slot is empty
        if self.data[index] is None:
            self.data[index] = new_node
        else:
            # Collision: Traverse the linked list at this index
            current = self.data[index]
            previous = None
            
            while current is not None:
                # Check for a duplicate key (update case)
                if current.key == key:
                    current.value.number = number 
                    return  
                
                previous = current
                current = current.next
            
            # If we reached the end of the list without finding a duplicate, 
            # append the new node to the end (separate chaining)
            if previous is not None:
                previous.next = new_node

    def search(self, key: str) -> Contact | None:
        index = self.hash_function(key)
        
        # Start at the head of the linked list for this index
        current = self.data[index]
        
        # Traverse the linked list
        while current is not None:
            if current.key == key:
                return current.value 
            current = current.next
            
        return None 

    def print_table(self) -> None:
        print("\n--- Hash Table Structure ---")
        for i in range(self.size):
            output = f"Index {i}: "
            current = self.data[i]
            
            if current is None:
                output += "Empty"
            else:
                nodes_data = []
                while current is not None:
                    nodes_data.append(str(current.value))
                    current = current.next
                
                # Format the output
                output += " - ".join(nodes_data)

            print(output)
        print("--------------------------")


# Test your hash table implementation here.  
print("--- Starting Hash Table Tests ---")
table = HashTable(10)

# Initial print
table.print_table()

# Add initial values
print("\n--- Inserting John and Rebecca ---")
table.insert("John", "909-876-1234")
table.insert("Rebecca", "111-555-0002")

# Print the new table structure 
table.print_table()

# Search for a value
contact = table.search("John") 
print("\nSearch result for 'John':", contact) 

# Edge Case #1 - Hash Collisions: Amy and May hash to the same index (index 5)
print("\n--- Inserting Amy and May (Collision Test) ---")
# 'Amy' hash: (65 + 109 + 121) % 10 = 295 % 10 = 5
# 'May' hash: (77 + 97 + 121) % 10 = 295 % 10 = 5
table.insert("Amy", "111-222-3333") 
table.insert("May", "222-333-1111") 
table.print_table()

# Edge Case #2 - Duplicate Keys: Update Rebecca's number
print("\n--- Updating Rebecca's Number ---")
table.insert("Rebecca", "999-444-9999") 
table.print_table()

# Final search for updated value
contact_updated = table.search("Rebecca")
print("\nSearch result for updated 'Rebecca':", contact_updated) 

# Edge Case #3 - Searching for a value not in the table
print("\nSearch result for 'Chris' (Not Found):", table.search("Chris"))