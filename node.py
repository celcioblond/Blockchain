from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from blockchain import Blockchain
from wallet import Wallet

app = FastAPI()
wallet = Wallet()
blockchain = Blockchain(wallet.public_key)

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/chain")
async def get_chain():
    chain_snapshot = blockchain.get_chain()
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]

    if not dict_chain:
        return JSONResponse(content={"error": "Empty chain"}, status_code=404)

    return JSONResponse(content=dict_chain, status_code=200)
