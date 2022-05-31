# Name: Adam Pruitt
# OSU Email: pruittad@oregonstate.edu
# Course: CS261 - Data Structures
# Assignment: 6
# Due Date: 6/3/22
# Description:A HashMap that uses open addressing with quadratic probing for collision resolution.


from a6_include import (DynamicArray, HashEntry,
                        hash_function_1, hash_function_2)


class HashMap:
    def __init__(self, capacity: int, function) -> None:
        """
        Initialize new HashMap that uses
        quadratic probing for collision resolution
        DO NOT CHANGE THIS METHOD IN ANY WAY
        """
        self._buckets = DynamicArray()
        for _ in range(capacity):
            self._buckets.append(None)

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
        """ A method that updates the key/value pair in the hash map.
        """
        if self.table_load() >= 0.5:
            self.resize_table(self._capacity * 2)
            buckets = self._buckets

        buckets = self._buckets
        hash = self._hash_function(key)
        index = hash % self._capacity
        entry = buckets.get_at_index(index)
        success = None
        jump = 1

        while success is not True:


            if entry is None:
                buckets.set_at_index(index, HashEntry(key, value))
                self._size += 1
                success = True
            elif entry.is_tombstone is True and entry.key == key:
                entry.value = value
                entry.is_tombstone = False
                self._size += 1
                success = True
            elif entry.key == key:
                entry.value = value
                entry.is_tombstone = False
                success = True
            else:
                index = hash % self._capacity
                index += (jump ** 2)
                if index > buckets.length() - 1:
                    index = index % self._capacity
                jump += 1
                entry = buckets.get_at_index(index)

    def table_load(self) -> float:
        """ A method that returns the current hash table load factor.
        """
        table_load = self._size / self._capacity
        return table_load

    def empty_buckets(self) -> int:
        """ A method that returns the number of empty buckets in the hash table.
        """
        buckets = self._buckets
        count = 0
        for index in range(0, buckets.length()):
            value = buckets.get_at_index(index)
            if value is not None:
                if value.is_tombstone is True:
                    count += 1
            else:
                count += 1

        return count

    def resize_table(self, new_capacity: int) -> None:
        """ A method that changes the capacity of the internal hash table.
        # remember to rehash non-deleted entries into new table
        """
        if new_capacity < 1 or new_capacity < self._size:
            return

        buckets = self._buckets
        new_table = DynamicArray()

        for index in range(0, new_capacity):
            new_table.append(None)
        self._buckets = new_table
        self._capacity = new_capacity
        self._size = 0

        for index in range(0, buckets.length()):
            bucket = buckets.get_at_index(index)
            if bucket is not None:
                if bucket.is_tombstone is False:
                    value = bucket.value
                    key = bucket.key
                    self.put(key, value)

    def get(self, key: str) -> object:
        """ A method that returns the value associated with the given key.
        """
        buckets = self._buckets
        hash = self._hash_function(key)
        index = hash % buckets.length()
        entry = buckets.get_at_index(index)
        success = None
        jump = 1

        while success is not True:
            if entry is None:
                return
            elif entry.is_tombstone is True:
                return
            elif entry.key == key:
                return entry.value
            else:
                index = hash % self._capacity
                index += (jump ** 2)
                if index > buckets.length() - 1:
                    index = index % self._capacity
                jump += 1
                entry = buckets.get_at_index(index)

    def contains_key(self, key: str) -> bool:
        """A method that searches for a given key in the hash map.
        """
        buckets = self._buckets
        hash = self._hash_function(key)
        index = hash % buckets.length()
        entry = buckets.get_at_index(index)
        success = None
        jump = 1

        if self._size == 0:
            return False

        while success is not True:
            if entry is None:
                return False
            elif entry.is_tombstone is True and entry.key == key:
                return False
            elif entry.key == key:
                return True
            else:
                index = hash % self._capacity
                index += (jump ** 2)
                if index > buckets.length() - 1:
                    index = index % self._capacity
                jump += 1
                entry = buckets.get_at_index(index)

    def remove(self, key: str) -> None:
        """ The method removes the given key and it's value from the hash map.
        """
        buckets = self._buckets
        hash = self._hash_function(key)
        index = hash % buckets.length()
        entry = buckets.get_at_index(index)
        success = None
        jump = 1

        while success is not True:
            if entry is None:
                return
            if self.contains_key(key) is False:
                return
            if entry.key == key and entry.is_tombstone is True:
                return
            if entry.key == key and entry.is_tombstone is False:
                entry.is_tombstone = True
                self._size -= 1
                success = True
            else:
                index = hash % self._capacity
                index += (jump ** 2)
                if index > buckets.length() - 1:
                    index = index % self._capacity
                jump += 1
                entry = buckets.get_at_index(index)

    def clear(self) -> None:
        """ A method that clears the contents of the hash map.
        """
        buckets = self._buckets
        for index in range(0, buckets.length()):
            buckets.set_at_index(index, None)
        self._size = 0

    def get_keys(self) -> DynamicArray:
        """ A method that returns a DynamicArray that contains all the keys stored in the hash map.
        """
        buckets = self._buckets
        keys = DynamicArray()
        for index in range(0, buckets.length()):
            bucket = buckets.get_at_index(index)
            if bucket is not None:
                if bucket.is_tombstone is False:
                    key = bucket.key
                    keys.append(key)
        return keys

# ------------------- BASIC TESTING ---------------------------------------- #

if __name__ == "__main__":

    m = HashMap(102, hash_function_1)
    print(m._size)
    m.put("key615", -237)
    m.remove('key615')
    m.put("key615", -237)
    m.put("key615", -869)
    m.put('key10', 10)
    m.put('key10', 12)
    m.put('key01', 10)
    m.put('key10', 13)
    m.put('key01', 13)
    m.put('key10', 14)
    m.put('key01', 14)
    m.contains_key('key01')
    m.remove('key01')
    m.remove('key10')
    m.put('key10', 13)
    m.put('key01', 13)
    m.put('key10', 14)
    m.put('key01', 14)
    m.contains_key('key01')
    print(m._size)


    print(m._size)
    m.put('key10', 5)
    print(m._size)
    m.remove('key10')
    m.put('key01', 12)
    print(m._size)

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

        if m.table_load() >= 0.5:
            print("Check that capacity gets updated during resize(); "
                  "don't wait until the next put()")

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
