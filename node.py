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


@app.post("/wallet")
def create_keys():
    wallet.create_keys()
    if wallet.save_keys():
        global blockchain
        blockchain = Blockchain(wallet.public_key)
        response = {
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance(),
        }
        return JSONResponse(content=response, status_code=201)
    else:
        response = {"message": "Saving the key failed"}
        return JSONResponse(content=response, status_code=500)


@app.get("/wallet")
def load_keys():
    global blockchain

    if not wallet.load_keys():
        return JSONResponse(
            content={"message": "Loading the keys failed"},
            status_code=500,
        )

    blockchain = Blockchain(wallet.public_key)

    return JSONResponse(
        content={
            "public_key": wallet.public_key,
            "private_key": wallet.private_key,
            "funds": blockchain.get_balance(),
        },
        status_code=201,
    )


@app.get("/balance")
async def get_balance():
    balance = blockchain.get_balance()
    if balance != None:
        response = {
            "message": "Fetched balance succesfully",
            "balance": balance,
        }
        return JSONResponse(content=response, status_code=200)
    else:
        response = {
            "message": "Loading balance failed",
            "wallet_set_up": wallet.public_key != None,
        }
        return JSONResponse(content=response, status_code=500)


@app.post("/mine")
async def mine():
    block = blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]
        response = {
            "message": "Block added successfully",
            "block": dict_block,
            "funds": blockchain.get_balance(),
        }
        return JSONResponse(content=response, status_code=201)
    else:
        response = {
            "message": "Adding a blocked failed",
            "wallet_set_up": wallet.public_key != None,
        }
        return JSONResponse(content=response, status_code=200)


@app.get("/chain")
async def get_chain():
    chain_snapshot = blockchain.get_chain()
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]

    if not dict_chain:
        return JSONResponse(content={"error": "Empty chain"}, status_code=404)

    return JSONResponse(content=dict_chain, status_code=200)
