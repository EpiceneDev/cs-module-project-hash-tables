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
        self.size = len(self.storage)



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
        # Your code here
        pass


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

        # hval = hval_init
        # for byte in data:
        #     hval = (hval * fnv_prime) % fnv_size
        #     hval = hval ^ _get_byte(byte)
        # return hval


    def djb2(self, key):
        """
        DJB2 hash, 32-bit

        Implement this, and/or FNV-1.
        """
        hash = 5381
        for char in key:
            hash = (hash * 33) + ord(char)
            print("HASH: ", hash)
        return hash


    def hash_index(self, key):
        """
        Take an arbitrary key and return a valid integer index
        between within the storage capacity of the hash table.
        """
        # return self.fnv1(key) % self.capacity
        print("hash_index: ", self.djb2(key) % self.capacity)
        return self.djb2(key) % self.capacity

    def put(self, key, value):
        """
        Store the value with the given key.

        Hash collisions should be handled with Linked List Chaining.

        Implement this.
        """
        # Your code here
        # my_list[my_hashing_func("aqua", len(my_list))] = "#00FFFF"
        ## 1. hash the word, get some number back from hash function
        index = self.hash_index(key)
        ## 2. modulo this number with array length to find the index
        ##    Being done by hash_index function
        ## 3. use index to insert word
        # self.storage[fnv1(self, key)] = value
        self.storage[index] = value
        print("PUT: ", value)
        return value

    def delete(self, key):
        """
        Remove the value stored with the given key.

        Print a warning if the key is not found.

        Implement this.
        """
        index = self.hash_index(key)
        self.storage[index] = None



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
        newKey = self.hash_index(key) 
        return self.storage[newKey]


    def resize(self, new_capacity):
        """
        Changes the capacity of the hash table and
        rehashes all key/value pairs.

        Implement this.
        """
        replacement = []

        if new_capacity >= self.capacity:
            addToList = [None] * (new_capacity - self.capacity)

            for i in addToList:
                self.storage.append(i)

            replacement = self.storage
            return replacement
        else:
            replacement = self.storage[:new_capacity]
            return replacement
        
        self.storage = replacement


        


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
