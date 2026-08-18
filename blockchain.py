#Initializing our blockchain list
blockchain = []
open_transactions = []
owner = "Celcio"

def get_last_blockchain_value():
  """Returns the last value of the blockchain"""
  if len(blockchain) < 1:
    return None
  return blockchain[-1]


def add_transaction(recipient, sender= owner, amount=1):
  """Append a new value and the last transaction to the blockchain"""
  transaction = {"sender": sender, "recipient": recipient, "value": amount}
  open_transactions.append(transaction)
  

def mine_block():
  """Add new block to blockchain"""
  pass


def get_transaction_value():
  """Gets the transaction amount from the user and returns it"""
  tx_sender = input("Enter the recipient of the transaction: ")
  tx_amount = float(input("Your transaction amount please: "))
  return (tx_sender, tx_amount)


def get_user_choice():
  user_input = input("Your choice: ")
  return user_input


def print_blockchain_elements():
  #Output the blockchain list
  for block in blockchain:
    print("Outputing block")
    print(block)


def verify_chain():
    is_valid = True
    for block_index in range(len(blockchain)):
      if block_index == 0:
        continue
      #Check the previous block vs the first element
      elif blockchain[block_index][0] == blockchain[block_index-1]:
        is_valid = True
      else:
        is_valid = False 
    return is_valid

waiting_for_input = True

while waiting_for_input:
  print('Please select an option: ')
  print("1: Add a new transaction value")
  print("2: Output the blockchains blocks")
  print("h: Manipulate the chain")
  print("e: Exit")
  user_choice = get_user_choice()
  if user_choice == "1":
    tx_data = get_transaction_value()
    recipient, amount = tx_data
    #Add transaction to the blockchain
    add_transaction(recipient, amount=amount)
    print(open_transactions)
  elif user_choice == "2":
    print_blockchain_elements()
  elif user_choice == "h":
    if len(blockchain) >= 1:
      blockchain[0] = [2]
  elif user_choice == "e":
    waiting_for_input = False
  else:
    print("Invalid input")
  if not verify_chain():
    print("Invalid blockchain")
    break

print('Completed')