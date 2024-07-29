import hashlib 
import json 
from time import time 

class Transactions:
   def __init__(self, sender, receiver, amount):
      self.sender = sender 
      self.receiver = receiver 
      self.amount = amount 
   
   def to_dict(self):
      return {
         "sender":self.sender,
         "receiver":self.receiver,
         "amount":self.amount 
      }
   
#define the block 
class Block:
   def __init__(self, index, timestamp, transactions, previous_hash):
      self.index = index 
      self.timestamp = timestamp 
      self.transactions = transactions 
      self.previous_hash = previous_hash 
      self.hash = self.calculate_hash()

   def calculate_hash(self):
      block_dict = {
         "index": self.index,
         "timestamp": self.timestamp,
         "transactions": [t.to_dict() for t in self.transactions], 
         "previous_hash": self.previous_hash 
      }
      block_string = json.dumps(block_dict, sort_keys=True).encode()
      return hashlib.sha256(block_string).hexdigest()

   def mine_block(self, difficulty):
      while self.hash[:difficulty] != '0' * difficulty:
         self.nonce += 1
         self.hash = self.calculate_hash()

   def __repr__(self):
      return json.dumps(self.__dict__, incident=4)

#defining the blockchain
class Blockchain:
   def __init__(self, difficulty=4):
      self.chain = [self.create_genesis_block()] 
      self.pending_transactions = []

   def create_genesis_block(self):
      return Block(0, time(), [], "0")

   def get_latest_block(self):
      return self.chain[-1]

   def add_block(self, new_block):
      new_block.previous_hash = self.get_latest_block().hash
      new_block.mine_block(self.difficulty)
      self.chain.append(new_block)
   
   def create_transactions(self,sender,receiver,amount):
      transaction = Transactions(sender, receiver, amount) 
      self.pending_transactions.append(transaction)  
   
   def mine_pending_transactions(self):
      latest_block = self.chain[-1]
      new_block = Block(
         len(self.chain),
         time(),
         self.pending_transactions,
         latest_block.hash 
      )
      self.chain.append(new_block)
      self.pending_transactions = []
      return new_block 

   def is_chain_valid(self):
      for  i in range(1, len(self.chain)):
         current_block = self.chain[i]
         previous_block = self.chain[i - 1]
         if current_block.hash != current_block.calculate_hash():
            return False 
         if current_block.previous_hash != previous_block.hash:
            return True 

my_blockchain = Blockchain()
transaction = Transactions("Alice", "Bob", 50)
my_blockchain.create_transactions(transaction.sender, transaction.receiver, transaction.amount)  