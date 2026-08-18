#Initializing our blockchain list
blockchain = []

def get_last_blockchain_value():
  """Returns the last value of the blockchain"""
  if len(blockchain) < 1:
    return None
  return blockchain[-1]


def add_value(transaction_amount, last_transaction=[1]):
  """Append a new value and the last transaction to the blockchain"""
  if last_transaction == None:
    last_transaction = [1]
  blockchain.append([last_transaction, transaction_amount])


def get_transaction_value():
  """Gets the transaction amount from the user and returns it"""
  user_input = float(input("Your transaction amount please: "))
  return user_input


def get_user_choice():
  user_input = input("Your choice: ")
  return user_input


def print_blockchain_elements():
  #Output the blockchain list
  for block in blockchain:
    print("Outputing block")
    print(block)

#Gets first transaction
tx_amount = get_transaction_value()
add_value(tx_amount)

while True:
  print('Please select an option: ')
  print("1: Add a new transaction value")
  print("2: Output the blockchains blocks")
  user_choice = get_user_choice()
  if user_choice == "1":
    tx_amount = get_transaction_value()
    add_value(tx_amount, get_last_blockchain_value())
  elif user_choice == "2":
    print_blockchain_elements()
  elif user_choice == "q":
    break
  else:
    print("Invalid input")

print('Completed')