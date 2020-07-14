class HashTableEntry:
    """
    Linked List hash table key/value pair
    """
    def __init__(self, key, value):
        self.key = key
        self.value = value
        self.next = None


# Hash table can't have fewer than this many slots
MIN_CAPACITY = 8


class HashTable:
    """
    A hash table that with `capacity` buckets
    that accepts string keys

    Implement this.
    """

    def __init__(self, capacity):

        self.capacity = capacity
        self.storage = [None] * capacity
        self.count = 0


    def get_num_slots(self):
        """
        Return the length of the list you're using to hold the hash
        table data. (Not the number of items stored in the hash table,
        but the number of slots in the main list.)

        One of the tests relies on this.

        Implement this.
        """
        return len(self.storage)

    def get_load_factor(self):
        """
        Return the load factor for this hash table.

        Implement this.
        """
        load = self.count / self.get_num_slots()
        return load


    def fnv1(self, key):
        """
        FNV-1 Hash, 64-bit

        Implement this, and/or DJB2.
        """
        # algorithm fnv-1 is
        #     hash := FNV_offset_basis do

        #     for each byte_of_data to be hashed
        #         hash := hash × FNV_prime
        #         hash := hash XOR byte_of_data

        #     return hash 
        
        # assert isinstance(data, bytes)


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash = 5381
        for char in key:
            # hash = (hash * 33) + ord(char)
            hash = (( hash << 5) + hash) + ord(char)
            # print("HASH: ", hash)
        return hash

        # hash_a = 5381
        # key_str_bytes = str.encode(key)
        # for x in key_str_bytes:
        #     hash_a = ((hash_a << 5) + hash_a) + x
        
        # return self._hash_mod(hash_a)


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # return self.fnv1(key) % self.storage
        # print("hash_index: ", self.djb2(key) % self.storage)
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        index = self.hash_index(key)

        current_node = self.storage[index]

        # Search for the key
        while current_node is not None and current_node.key != key:
            current_node = current_node.next 
        # When the key if found, insert value if the node already
        # has value.. As it is already optimized (load factor) and just 
        # needs to be inserted in the table TODO ask Jose
        if current_node is not None:
            # print('CURRENT NODE: ', current_node)

            current_node.value = value
            self.count += 1
        # else create the node, insert the value and check the load value.
        else:
            new_node = HashTableEntry(key, value)
            new_node.next = self.storage[index]
            self.storage[index] = new_node 

            print(f"new_node = {new_node}  storage = {self.storage[index]}/n")
            self.count += 1 

            if self.get_load_factor() > 0.7:
                self.resize(self.capacity * 2)  


    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)

        current_node = self.storage[index]

        last_node = None

        while current_node is not None and current_node.key != key:
            current_node = current_node.next 

        if current_node is None:
            print("ERROR: Unable to remove node with key " + key)
        else:
            if last_node is None:
                self.storage[index] = current_node.next
            else:
                last_node.next = current_node.next
            if self.get_load_factor() < 0.2:
                if self.capacity > MIN_CAPACITY:
                    new_capacity = self.capacity // 2
                    if new_capacity < MIN_CAPACITY:
                        new_capacity = MIN_CAPACITY
                    self.resize(new_capacity)





    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        index = self.hash_index(key) 
        
        node = self.storage[index]

        while node:
            if node.key == key:
                return node.value
            node = node.next



    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        
        if self.count / self.capacity > 0.7:
            # double capacity
            temp_list = []
            for a in self.storage:
                node = a
                while node:
                    temp_list.append([node.key, node.value])
                    node = node.next

            self.capacity = 2 * self.capacity
            self.storage = [None] * self.capacity

            for b in temp_list:
                self.put(b[0], b[1])
                self.count -= 1

            # shrink capacity
        if self.count / self.capacity < 0.2:
            temp_list = []
            for a in self.storage:
                node = a
                while node:
                    temp_list.append([node.key, node.value])
                    node = node.next

            self.capacity = self.capacity // 2
            self.storage = [None] * self.capacity




if __name__ == "__main__":
    ht = HashTable(8)

    ht.put("line_1", "'Twas brillig, and the slithy toves")
    ht.put("line_2", "Did gyre and gimble in the wabe:")
    ht.put("line_3", "All mimsy were the borogoves,")
    ht.put("line_4", "And the mome raths outgrabe.")
    ht.put("line_5", '"Beware the Jabberwock, my son!')
    ht.put("line_6", "The jaws that bite, the claws that catch!")
    ht.put("line_7", "Beware the Jubjub bird, and shun")
    ht.put("line_8", 'The frumious Bandersnatch!"')
    ht.put("line_9", "He took his vorpal sword in hand;")
    ht.put("line_10", "Long time the manxome foe he sought--")
    ht.put("line_11", "So rested he by the Tumtum tree")
    ht.put("line_12", "And stood awhile in thought.")

    print("")

    # Test storing beyond capacity
    for i in range(1, 13):
        print(ht.get(f'line_{i}'))

    # Test resizing
    old_capacity = ht.get_num_slots()
    ht.resize(ht.capacity * 2)
    new_capacity = ht.get_num_slots()

    print(f"\nResized from {old_capacity} to {new_capacity}.\n")

    # Test if data intact after resizing
    for i in range(1, 13):
        print(ht.get(f"line_{i}"))

    print("")
