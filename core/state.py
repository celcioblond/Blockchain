import os

from models.blockchain import Blockchain
from models.wallet import Wallet

# The node id comes from the port the node was launched with. It is passed
# through the environment so it also survives uvicorn's reloader subprocess.
NODE_ID = os.environ.get("NODE_ID", "5000")

wallet = Wallet(NODE_ID)
blockchain = Blockchain(wallet.public_key, NODE_ID)
