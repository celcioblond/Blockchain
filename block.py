import time as time_module

from utility.printable import Printable


class Block(Printable):
    def __init__(self, index, previous_hash, transactions, proof, time=None):
        self.index = index
        self.previous_hash = previous_hash
        self.timestamp = time if time is not None else time_module.time()
        self.transactions = transactions
        self.proof = proof
