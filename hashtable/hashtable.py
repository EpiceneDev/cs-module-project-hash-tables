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
        load = self.count / self.get_num_slots


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
            print("HASH: ", hash)
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
        return self.djb2(key) % self.storage

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        index = self.hash_index(key)

        if self.storage[index]:
            node = self.storage[index]

            while node:
                if node.key == key:
                    node.value = value
                    break
                elif node.next:
                    node = node.next
                else:
                    node.next = HashTableEntry(key, value)
                    self.count += 1
                    self.resize()
                    break

        else:
            self.storage[index] = HashTableEntry(key, value)
            self.count += 1
            self.resize()
        # ## 1. hash the word, get some number back from hash function
        # ## 2. modulo this number with array length to find the index
        # ##    Being done by hash_index function
        # index = self.hash_index(key)
        # ## 3. use index to insert word
        # # self.storage[fnv1(self, key)] = value
        # # if self.storage[index] != None:
        # #     self.storage[index] 
        # #     cur_value = self.storage[index]
        # cur_value = self.storage[index]
        # # if there are no contents or cur_value is equal to none, 
        # # If the value of the list at the hash function’s returned index is empty, a new 
        # # linked list is created with the value as the first element of the linked list.
        # ## if the currrent value at the index is empty, 
        # ## start the liked list with the key value pair at this index
        # if cur_value is None:
        #     self.storage[index] = HashTableEntry(key, value)
        #     return

        # ## if the current value has contents, check if 
        # if cur_value.key == key:
        #     self.storage[index] = HashTableEntry(key, value)
                
            
        #     ## make the head the current hashed key
        #     ## put into the tail the new key

        #     self.storage[index] = value
        # print("PUT: ", value)
        # return value

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)

        if not self.storage(index):
            print("NO KEY FOUND!")
            return

        node = self.storage(index)

        prev_node = None

        while node:
            if node.key == key:
                if prev_node:
                    if node.next:
                        prev_node.next = node.next
                    else:
                        prev_node.next = None
                else:
                    if node.next:
                        self.storage[index] = node.next
                    else self.storage[index] = None
                
                temp = node
                self.count -= 1
                self.resize()
                return temp.value

            elif node.next:
                prev_node = node
                node = node.next
            else:
                print("NO KEY FOUND!")
                return



    def get(self, key):
        """
        Retrieve the value stored with the given key.

        Returns None if the key is not found.

        Implement this.
        """
        # steps to get
        ## 1. hash the key/word, get number back from hash function
        ## 2. modulo with array length to find index
        ## 3. look up value at that index, return it
        index = self.hash_index(key) 
        
        if not self.storage[index]:
            return None
        else:
            node = self.storage[index]
            while node:
                if node.key == key:
                    return node.value
                node = node.next
            return None


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
