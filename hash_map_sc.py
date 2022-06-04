# Name: Adam Pruitt
# OSU Email: pruittad@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/3/22
# Description: A hashmap that uses chaining for collision resolution. It uses a single linked list.


from a6_include import (DynamicArray, LinkedList,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        separate chaining for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(LinkedList())

        self._capacity = capacity
        self._hash_function = function
        self._size = 0

    def __str__(self) -> str:
        """
        Override string method to provide more readable output
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        out = ''
        for i in range(self._buckets.length()):
            out += str(i) + ': ' + str(self._buckets[i]) + '\n'
        return out

    def get_size(self) -> int:
        """
        Return size of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._size

    def get_capacity(self) -> int:
        """
        Return capacity of map
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        return self._capacity

    # ------------------------------------------------------------------ #

    def put(self, key: str, value: object) -> None:
        """ A method that updates the key/value pair in the hash map. If it exists it is replaced with a new value.
        If it's not in the map than it should be added.
        """

        buckets = self._buckets
        hash = self._hash_function(key)
        index = hash % buckets.length()
        linked_hash = buckets.get_at_index(index)
        node = linked_hash.contains(key)                # Searches if the key is found at that index.

        # If contains comes back as True the key and value are changed.
        if node is not None:
            node.key = key
            node.value = value

        # Otherwise, a new node is inserted.
        else:
            linked_hash.insert(key, value)
            self._size += 1

    def empty_buckets(self) -> int:
        """ A method that returns the number of empty buckets in the hash table.
        """
        buckets = self._buckets
        empty_buckets = 0

        # Looping through the whole array. If a bucket is empty 1 is added to the count.
        for index in range(0, buckets.length()):
            if buckets.get_at_index(index).length() == 0:
                empty_buckets += 1

        return empty_buckets

    def table_load(self) -> float:
        """ A method that returns the current hash table load factor. It is calculated by the size divided by
        the capacity.
        """
        table_load = self._size / self._capacity
        return table_load

    def clear(self) -> None:
        """ A method that clears the contents of the hash map.
        """
        buckets = self._buckets
        new_list = LinkedList()

        # Loops through all the buckets. If a bucket has nodes with values, it is replaced with an empty linked list.
        for index in range(0, buckets.length()):
            if buckets.get_at_index(index).length() != 0:
                buckets.set_at_index(index, new_list)
        capacity = self.get_capacity()
        self._size = 0                                      # Resets the size to zero.

    def resize_table(self, new_capacity: int) -> None:
        """ A method that changes the capacity of the internal hash table.
        """
        buckets = self._buckets
        new_hash = DynamicArray()

        # If the new_capacity is less than one nothing happens.
        if new_capacity < 1:
            return

        # Creates a new linked list based on the new_capacity.
        for index in range(0, new_capacity):
            link = LinkedList()
            new_hash.append(link)

        # Adds only the nodes that have keys and values to the new array.
        for index in range(0, buckets.length()):
            count = buckets.get_at_index(index).length()
            bucket = buckets.get_at_index(index)
            if count != 0:
                for node in bucket:
                    key = node.key
                    value = node.value
                    hash = self._hash_function(key)
                    new_index = hash % new_hash.length()
                    linked_hash = new_hash.get_at_index(new_index)
                    linked_hash.insert(key, value)
                    count -= 1

        # Replaces the old hash with the new one.
        self._buckets = new_hash
        self._capacity = new_capacity

    def get(self, key: str) -> object:
        """ A method that returns the value associated with a given key.
        """
        buckets = self._buckets
        hash = self._hash_function(key)
        index = hash % buckets.length()

        # If the bucket has nothing in it return None.
        if buckets.get_at_index(index).length() == 0:
            return None

        # Otherwise, check to see if that bucket contains the key. If it does return the value.
        else:
            link = buckets.get_at_index(index)
            node = link.contains(key)
            if node is None:
                return None
            return node.value

    def contains_key(self, key: str) -> bool:
        """ A method that returns True if the given key is found in the hash map.
        """
        buckets = self._buckets
        hash = self._hash_function(key)
        index = hash % buckets.length()

        if buckets.length() == 0:
            return False
        if buckets.get_at_index(index).length() == 0:
            return False

        # If there is something in the bucket then check to see if the key is in there. If it is then return the value.
        else:
            link = buckets.get_at_index(index)
            node = link.contains(key)
            if node is None:
                return False
            return True

    def remove(self, key: str) -> None:
        """ A method that removes a given key and it's value from the hash map.
        """
        buckets = self._buckets
        hash = self._hash_function(key)
        index = hash % buckets.length()
        link = buckets.get_at_index(index)
        node = link.contains(key)

        # If the key is not in that bucket return None.
        if node is None:
            return
        # Otherwise, remove th key and decrease the size.
        else:
            link.remove(key)
            self._size -= 1

    def get_keys(self) -> DynamicArray:
        """ A method that returns a DynamicArray of all the keys in the hash.
        """
        hash_table = self._buckets
        array = DynamicArray()

        # Looping through the whole array. If the bucket isn't empty then loop through the bucket adding each key
        # in the bucket.
        for index in range(0, hash_table.length()):
            if hash_table.get_at_index(index).length() > 0:
                bucket = hash_table.get_at_index(index)
                length = bucket.length()
                for node in bucket:
                    array.append(node.key)
                    length -= 1
        return array

def find_mode(da: DynamicArray) -> (DynamicArray, int):
    """ A function that will return a tuple containing the value/s that appear with the highest frequency and the
    frequency at which they occur.
    """
    map = HashMap(da.length() // 3, hash_function_1)
    stored_count = 0
    mode_array = DynamicArray()

    # Looping through all of the indices.
    for index in range(0, da.length()):

        # If the map doesn't contain the key it adds the key to that index, and it's value is one. If the count is the
        # same as the stored count add it to the array. If it's greater empty the current node_array add the key/value.
        if map.contains_key(da.get_at_index(index)) is False:
            count = 1
            map.put(da.get_at_index(index), count)
            if count == stored_count:
                mode_array.append(da.get_at_index(index))
            elif count > stored_count:
                mode_array = DynamicArray()
                mode_array.append(da.get_at_index(index))
                stored_count = count

        # Otherwise, update the key's value by adding one to it. Then if it's equal to the current count add it to the
        # array. If it's greater than the current count empty the current node_array and add the key and value.
        else:
            count = map.get(da.get_at_index(index))
            map.put(da.get_at_index(index), count + 1)
            count += 1
            if count == stored_count:
                mode_array.append(da.get_at_index(index))
            elif count > stored_count:
                mode_array = DynamicArray()
                mode_array.append(da.get_at_index(index))
                stored_count = count

    return mode_array, stored_count


# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    print("\nPDF - put example 1")
    print("-------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('str' + str(i), i * 100)
        if i % 25 == 24:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - put example 2")
    print("-------------------")
    m = HashMap(40, hash_function_2)
    for i in range(50):
        m.put('str' + str(i // 3), i * 100)
        if i % 10 == 9:
            print(m.empty_buckets(), m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 1")
    print("-----------------------------")
    m = HashMap(100, hash_function_1)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key1', 30)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())
    m.put('key4', 40)
    print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - empty_buckets example 2")
    print("-----------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(150):
        m.put('key' + str(i), i * 100)
        if i % 30 == 0:
            print(m.empty_buckets(), m.get_size(), m.get_capacity())

    print("\nPDF - table_load example 1")
    print("--------------------------")
    m = HashMap(100, hash_function_1)
    print(m.table_load())
    m.put('key1', 10)
    print(m.table_load())
    m.put('key2', 20)
    print(m.table_load())
    m.put('key1', 30)
    print(m.table_load())

    print("\nPDF - table_load example 2")
    print("--------------------------")
    m = HashMap(50, hash_function_1)
    for i in range(50):
        m.put('key' + str(i), i * 100)
        if i % 10 == 0:
            print(m.table_load(), m.get_size(), m.get_capacity())

    print("\nPDF - clear example 1")
    print("---------------------")
    m = HashMap(100, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key1', 30)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - clear example 2")
    print("---------------------")
    m = HashMap(50, hash_function_1)
    print(m.get_size(), m.get_capacity())
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity())
    m.put('key2', 20)
    print(m.get_size(), m.get_capacity())
    m.resize_table(100)
    print(m.get_size(), m.get_capacity())
    m.clear()
    print(m.get_size(), m.get_capacity())

    print("\nPDF - resize example 1")
    print("----------------------")
    m = HashMap(20, hash_function_1)
    m.put('key1', 10)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))
    m.resize_table(30)
    print(m.get_size(), m.get_capacity(), m.get('key1'), m.contains_key('key1'))

    print("\nPDF - resize example 2")
    print("----------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 13)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())

    for capacity in range(111, 1000, 117):
        m.resize_table(capacity)

        m.put('some key', 'some value')
        result = m.contains_key('some key')
        m.remove('some key')

        for key in keys:
            # all inserted keys must be present
            result &= m.contains_key(str(key))
            # NOT inserted keys must be absent
            result &= not m.contains_key(str(key + 1))
        print(capacity, result, m.get_size(), m.get_capacity(), round(m.table_load(), 2))

    print("\nPDF - get example 1")
    print("-------------------")
    m = HashMap(30, hash_function_1)
    print(m.get('key'))
    m.put('key1', 10)
    print(m.get('key1'))

    print("\nPDF - get example 2")
    print("-------------------")
    m = HashMap(150, hash_function_2)
    for i in range(200, 300, 7):
        m.put(str(i), i * 10)
    print(m.get_size(), m.get_capacity())
    for i in range(200, 300, 21):
        print(i, m.get(str(i)), m.get(str(i)) == i * 10)
        print(i + 1, m.get(str(i + 1)), m.get(str(i + 1)) == (i + 1) * 10)

    print("\nPDF - contains_key example 1")
    print("----------------------------")
    m = HashMap(10, hash_function_1)
    print(m.contains_key('key1'))
    m.put('key1', 10)
    m.put('key2', 20)
    m.put('key3', 30)
    print(m.contains_key('key1'))
    print(m.contains_key('key4'))
    print(m.contains_key('key2'))
    print(m.contains_key('key3'))
    m.remove('key3')
    print(m.contains_key('key3'))

    print("\nPDF - contains_key example 2")
    print("----------------------------")
    m = HashMap(75, hash_function_2)
    keys = [i for i in range(1, 1000, 20)]
    for key in keys:
        m.put(str(key), key * 42)
    print(m.get_size(), m.get_capacity())
    result = True
    for key in keys:
        # all inserted keys must be present
        result &= m.contains_key(str(key))
        # NOT inserted keys must be absent
        result &= not m.contains_key(str(key + 1))
    print(result)

    print("\nPDF - remove example 1")
    print("----------------------")
    m = HashMap(50, hash_function_1)
    print(m.get('key1'))
    m.put('key1', 10)
    print(m.get('key1'))
    m.remove('key1')
    print(m.get('key1'))
    m.remove('key4')

    print("\nPDF - get_keys example 1")
    print("------------------------")
    m = HashMap(10, hash_function_2)
    for i in range(100, 200, 10):
        m.put(str(i), str(i * 10))
    print(m.get_keys())

    m.resize_table(1)
    print(m.get_keys())

    m.put('200', '2000')
    m.remove('100')
    m.resize_table(2)
    print(m.get_keys())

    print("\nPDF - find_mode example 1")
    print("-----------------------------")
    da = DynamicArray(["apple", "apple", "grape", "melon", "melon", "peach"])
    map = HashMap(da.length() // 3, hash_function_1)
    mode, frequency = find_mode(da)
    print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}")

    print("\nPDF - find_mode example 2")
    print("-----------------------------")
    test_cases = (
        ["Arch", "Manjaro", "Manjaro", "Mint", "Mint", "Mint", "Ubuntu", "Ubuntu", "Ubuntu", "Ubuntu"],
        ["one", "two", "three", "four", "five"],
        ["2", "4", "2", "6", "8", "4", "1", "3", "4", "5", "7", "3", "3", "2"]
    )

    for case in test_cases:
        da = DynamicArray(case)
        map = HashMap(da.length() // 3, hash_function_2)
        mode, frequency = find_mode(da)
        print(f"Input: {da}\nMode: {mode}, Frequency: {frequency}\n")
