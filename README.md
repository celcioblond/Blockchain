# Python Blockchain

A peer-to-peer blockchain built with FastAPI. Each node has its own RSA wallet, mines blocks with proof of work, and syncs transactions and blocks with its peers.

## Features

- RSA wallets with signed transactions
- Proof-of-work mining with rewards
- Transactions and blocks broadcast to peer nodes
- Conflict resolution (longest valid chain wins)
- Per-node persistence in `data/`

## Setup

```bash
python -m venv venv
venv\Scripts\activate        # Windows
pip install -r requirements.txt
```

## Run

```bash
python main.py -p 5000
python main.py -p 5001       # another node
```

Interactive API docs are available at `http://localhost:<port>/docs`.

## Endpoints

| Method | Path | Description |
| --- | --- | --- |
| POST / GET | `/wallet` | Create / load wallet keys |
| GET | `/balance` | Wallet balance |
| POST / GET | `/transaction` | Create / list open transactions |
| POST | `/mine` | Mine a block |
| GET | `/chain` | Full blockchain |
| POST | `/resolve-conflicts` | Replace chain with the longest valid peer chain |
| POST / GET | `/node` | Add / list peer nodes |
| DELETE | `/node/{node_url}` | Remove a peer node |
| POST | `/broadcast-transaction`, `/broadcast-block` | Used internally between nodes |

## Quick start (two nodes)

1. `POST /wallet` on both nodes.
2. Connect them: `POST /node` with `{"node": "localhost:5001"}` on 5000, and `{"node": "localhost:5000"}` on 5001.
3. `POST /mine` on 5000, then `GET /chain` on 5001 to see the synced block.
