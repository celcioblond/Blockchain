class Node:

    def __init__(self):
        self.blockchain = []

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
        for block in self.blockchain:
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
                self.print_blockchain_elements()

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
                self.print_blockchain_elements()
                print("Invalid blockchain")
                break

            print("Balance of {}: {:6.2f}".format("Celcio", get_balance("Celcio")))

    print("Completed")
