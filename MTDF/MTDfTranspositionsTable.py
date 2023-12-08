from. import (HashMTDfEntry)
#import HashMTDfEntry


class TranspostionTable:
    def __init__(self, size):
        self.size = size
        self.table = [None] * (1 << self.size)
        #self.table = [None] * (2**32)

    def storeEntry(self, entry: HashMTDfEntry.HashEntry):
        hash = entry.getHash()
        index = abs(hash % (1 << self.size))
        #index = abs(hash % (2**32))
        self.table[index] = entry

    def storeLowerbound(self, hash, depth, Lowerbound: float):
        entry = self.probeEntry(hash)
        if entry:
             entry.Lowerbound = Lowerbound
        else:
            entry = HashMTDfEntry.HashEntry(hash, depth, Lowerbound, None)
        self.storeEntry(entry)

    def storeUpperbound(self, hash, depth, Upperbound: float):
        entry = self.probeEntry(hash)
        #if entry != None:
        if entry:
             entry.Upperbound = Upperbound
        else:
            entry = HashMTDfEntry.HashEntry(hash, depth, None, Upperbound)
        self.storeEntry(entry)

    def probeEntry(self, hash) -> HashMTDfEntry.HashEntry:
        index = abs(hash % (1 << self.size))
        #index = abs(hash % (2 ** 32))
        result = self.table[index]
        return result
