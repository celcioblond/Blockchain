# Initializing our blockchain list

genesis_block = {
    "previous_hash": "",
    "index": 0,
    "transactions": [],
}

blockchain = [genesis_block]
open_transactions = []
owner = "Celcio"
participants = {'Celcio'}

def hash_block(block):
    return ''.join([str(block[key]) for key in block])

def get_last_blockchain_value():
    """Returns the last value of the blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def add_transaction(recipient, sender=owner, amount=1):
    """Append a new value and the last transaction to the blockchain"""
    transaction = {"sender": sender, "recipient": recipient, "value": amount}
    open_transactions.append(transaction)
    participants.add(sender)
    participants.add(recipient)

def mine_block():
    """Add new block to blockchain"""
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    for key in last_block:
        value = last_block[key]
        hashed_block = hashed_block + str(value)
    block = {
        "previous_hash": hashed_block,
        "index": len(blockchain),
        "transactions": open_transactions,
    }
    blockchain.append(block)


def get_transaction_value():
    """Gets the transaction amount from the user and returns it"""
    tx_sender = input("Enter the recipient of the transaction: ")
    tx_amount = float(input("Your transaction amount please: "))
    return (tx_sender, tx_amount)


def get_user_choice():
    user_input = input("Your choice: ")
    return user_input


def print_blockchain_elements():
    # Output the blockchain list
    for block in blockchain:
        print("Outputing block")
        print(block)


def verify_chain():
    """Verify the current blockchain """
    for (index, block) in enumerate(blockchain):
        if index == 0:
          continue
        if block['previous_hash'] != hash_block(blockchain[index - 1]):
          return False
    return True


waiting_for_input = True

while waiting_for_input:
    print("Please select an option: ")
    print("1: Add a new transaction value")
    print("2: Mine a new block")
    print("3: Output the blockchains blocks")
    print("4: Output participants")
    print("h: Manipulate the chain")
    print("e: Exit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        # Add transaction to the blockchain
        add_transaction(recipient, amount=amount)
        print(open_transactions)
    elif user_choice == "2":
        mine_block()
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        print(participants)
    elif user_choice == "h":
        if len(blockchain) >= 1:
            blockchain[0] = {
                'previous_hash': '',
                'index': 0,
                'transaction': [{'sender': 'Max', 'recipient': 'Celcio', 'amount': 100}]
            }
    elif user_choice == "e":
        waiting_for_input = False
    else:
        print("Invalid input")
    if not verify_chain():
        print_blockchain_elements()
        print("Invalid blockchain")
        break

print("Completed")
