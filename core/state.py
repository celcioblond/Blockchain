from models.blockchain import Blockchain
from models.wallet import Wallet

wallet = Wallet()
blockchain = Blockchain(wallet.public_key)
