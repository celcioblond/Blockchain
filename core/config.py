import os

MINING_REWARD = 10

# Per-node data lives in its own folder so the dev reloader (which watches the
# project directory) is not restarted every time a node saves its chain.
PROJECT_ROOT = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
DATA_DIR = os.path.join(PROJECT_ROOT, "data")
os.makedirs(DATA_DIR, exist_ok=True)

WALLET_FILE = os.path.join(DATA_DIR, "wallet-{}.txt")
BLOCKCHAIN_FILE = os.path.join(DATA_DIR, "blockchain-{}.txt")

CORS_ORIGINS = ["*"]
