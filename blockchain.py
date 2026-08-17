#Initializing our blockchain list
blockchain = []

def get_last_blockchain_value():
  """Returns the last value of the blockchain"""
  return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
  """Append a new value and the last transaction to the blockchain"""
  blockchain.append([last_transaction, transaction_amount])


def get_user_input():
  """Gets the input from the user and returns it"""
  user_input = float(input("Your transaction amount please: "))
  return user_input

#Gets first transaction
tx_amount = get_user_input()
add_value(tx_amount)

#Gets second transaction
tx_amount = get_user_input()
add_value(last_transaction=get_last_blockchain_value(),
           transaction_amount=tx_amount)

#Get thrd transaction
tx_amount = get_user_input()
add_value(tx_amount, get_last_blockchain_value())

print(blockchain)