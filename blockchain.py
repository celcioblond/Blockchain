import hashlib
import json
import pickle
from collections import OrderedDict
from functools import reduce

from block import Block
from hash_util import hash_block
from transaction import Transaction
from verification import Verification

# Initializing our blockchain list
MINING_REWARD = 10

blockchain = []
open_transactions = []
owner = "Celcio"


def load_data():
    global blockchain
    global open_transactions
    try:
        with open("blockchain.txt", mode="r") as f:
            # file_content = pickle.load(f.read())

            file_content = f.readlines()

            blockchain = json.loads(file_content[0][:-1])

            updated_blockchain = []

            for block in blockchain:
                converted_tx = [
                    Transaction(tx["sender"], tx["recipient"], tx["amount"])
                    for tx in block["transactions"]
                ]
                updated_block = Block(
                    block["index"],
                    block["previous_hash"],
                    converted_tx,
                    block["proof"],
                    block["timestamp"],
                )

                updated_blockchain.append(updated_block)

            blockchain = updated_blockchain

            open_transactions = json.loads(file_content[1])

            updated_transactions = []

            for tx in open_transactions:
                updated_transaction = Transaction(
                    tx["sender"], tx["recipient"], tx["amount"]
                )
                updated_transactions.append(updated_transaction)

            open_transactions = updated_transactions

    except (IOError, IndexError):
        genesis_block = Block(0, "", [], 100, 0)
        blockchain = [genesis_block]
        open_transactions = []

    finally:
        print("Cleanup")


load_data()


def save_data():
    try:
        with open("blockchain.txt", mode="w") as f:
            saveable_chain = [
                block.__dict__
                for block in [
                    Block(
                        block_el.index,
                        block_el.previous_hash,
                        [tx.__dict__ for tx in block_el.transactions],
                        block_el.proof,
                        block_el.timestamp,
                    )
                    for block_el in blockchain
                ]
            ]
            f.write(json.dumps(saveable_chain))
            f.write("\n")
            saveable_tx = [tx.__dict__ for tx in open_transactions]
            f.write(json.dumps(saveable_tx))
            # saved_data = {
            #     'chain': blockchain,
            #     'ot': open_transactions
            # }
            # f.write(pickle.dumps(saved_data))
    except IOError:
        print("Saving failed")


def get_balance(participant):
    tx_sender = [
        [tx.amount for tx in block.transactions if tx.sender == participant]
        for block in blockchain
    ]
    open_tx_sender = [tx.amount for tx in open_transactions if tx.sender == participant]
    tx_sender.append(open_tx_sender)
    amount_sent = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,
        tx_sender,
        0,
    )
    tx_recipient = [
        [tx.amount for tx in block.transactions if tx.recipient == participant]
        for block in blockchain
    ]
    amount_received = reduce(
        lambda tx_sum, tx_amt: tx_sum + sum(tx_amt) if len(tx_amt) > 0 else tx_sum + 0,
        tx_recipient,
        0,
    )
    return amount_received - amount_sent


def get_last_blockchain_value():
    """Returns the last value of the blockchain"""
    if len(blockchain) < 1:
        return None
    return blockchain[-1]


def proof_of_work():
    last_block = blockchain[-1]
    last_hash = hash_block(last_block)
    proof = 0
    verifier = Verification()
    while not verifier.valid_proof(open_transactions, last_hash, proof):
        proof += 1
    return proof


def add_transaction(recipient, sender=owner, amount=1):
    """Append a new value and the last transaction to the blockchain"""
    # transaction = {"sender": sender, "recipient": recipient, "amount": amount}
    transaction = Transaction(sender, recipient, amount)
    verifier = Verification()
    if verifier.verify_transaction(transaction, get_balance):
        open_transactions.append(transaction)
        save_data()
        return True
    return False


def mine_block():
    """Add new block to blockchain"""
    last_block = blockchain[-1]
    hashed_block = hash_block(last_block)
    proof = proof_of_work()
    # reward_transaction = {
    #     'sender': 'MINING',
    #     'recipient': owner,
    #     'amount': MINING_REWARD,
    # }
    reward_transaction = Transaction("MINING", owner, MINING_REWARD)
    copied_transactions = open_transactions[:]
    copied_transactions.append(reward_transaction)
    block = Block(len(blockchain), hashed_block, copied_transactions, proof)
    blockchain.append(block)
    return True


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


waiting_for_input = True

while waiting_for_input:
    print("Please select an option: ")
    print("1: Add a new transaction value")
    print("2: Mine a new block")
    print("3: Output the blockchains blocks")
    print("4: Check transaction validity")
    print("e: Exit")
    user_choice = get_user_choice()
    if user_choice == "1":
        tx_data = get_transaction_value()
        recipient, amount = tx_data
        # Add transaction to the blockchain
        if add_transaction(recipient, amount=amount):
            print("Added transaction")
        else:
            print("Transaction failed")
        print(open_transactions)
    elif user_choice == "2":
        if mine_block():
            open_transactions = []
            save_data()
    elif user_choice == "3":
        print_blockchain_elements()
    elif user_choice == "4":
        verifier = Verification()
        if verifier.verify_transactions(open_transactions, get_balance):
            print("All transactions are valid")
        else:
            print("There are invalid transactions")
    elif user_choice == "e":
        waiting_for_input = False
    else:
        print("Invalid input")
    verifier = Verification()
    if not verifier.verify_chain(blockchain):
        print_blockchain_elements()
        print("Invalid blockchain")
        break
    print("Balance of {}: {:6.2f}".format("Celcio", get_balance("Celcio")))

print("Completed")
