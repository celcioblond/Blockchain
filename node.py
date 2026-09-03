from uuid import uuid4

from blockchain import Blockchain
from verification import Verification


class Node:

    def __init__(self):
        self.id = str(uuid4())
        self.blockchain = Blockchain(self.id)

    def get_transaction_value(self):
        """Gets the transaction amount from the user and returns it"""
        tx_sender = input("Enter the recipient of the transaction: ")
        tx_amount = float(input("Your transaction amount please: "))
        return (tx_sender, tx_amount)

    def get_user_choice(self):
        user_input = input("Your choice: ")
        return user_input

    def print_blockchain_elements(self):
        # Output the blockchain list
        for block in self.blockchain.get_chain():
            print("Outputing block")
            print(block)

    def listen_for_input(self):
        waiting_for_input = True

        while waiting_for_input:
            print("Please select an option: ")
            print("1: Add a new transaction value")
            print("2: Mine a new block")
            print("3: Output the blockchains blocks")
            print("4: Check transaction validity")
            print("e: Exit")

            user_choice = self.get_user_choice()

            if user_choice == "1":
                tx_data = self.get_transaction_value()
                recipient, amount = tx_data

                # Add transaction to the blockchain
                if self.blockchain.add_transaction(recipient, self.id, amount=amount):
                    print("Added transaction")
                else:
                    print("Transaction failed")

                print(self.blockchain.get_open_transactions())

            elif user_choice == "2":
                self.blockchain.mine_block()
                print("Block mined successfully")
            elif user_choice == "3":
                self.print_blockchain_elements()
            elif user_choice == "4":
                if Verification.verify_transactions(
                    self.blockchain.get_open_transactions(), self.blockchain.get_balance
                ):
                    print("All transactions are valid")
                else:
                    print("There are invalid transactions")

            elif user_choice == "e":
                waiting_for_input = False

            else:
                print("Invalid input")

            if not Verification.verify_chain(self.blockchain.get_chain()):
                self.print_blockchain_elements()
                print("Invalid blockchain")
                break

            print(
                "Balance of {}: {:6.2f}".format(self.id, self.blockchain.get_balance())
            )

    print("Completed")


node = Node()
node.listen_for_input()
