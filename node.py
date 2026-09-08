from fastapi import FastAPI, HTTPException
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from blockchain import Blockchain
from models.transaction_request import TransactionRequest
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
async def create_keys():
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
        raise HTTPException(status_code=404, detail="Saving the key failed")


@app.get("/wallet")
async def load_keys():
    global blockchain

    if not wallet.load_keys():
        raise HTTPException(status_code=500, detail="Loading the keys failed")

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
        raise HTTPException(
            status_code=500,
            detail={
                "message": "Loading balance failed",
                "wallet_set_up": wallet.public_key != None,
            },
        )


@app.post("/transaction")
async def add_transaction(transaction: TransactionRequest):
    if wallet.public_key is None:
        raise HTTPException(status_code=400, detail="No wallet set up")

    signature = wallet.sign_transaction(
        wallet.public_key, transaction.recipient, transaction.amount
    )
    success = blockchain.add_transaction(
        transaction.recipient, wallet.public_key, signature, transaction.amount
    )

    if not success:
        raise HTTPException(status_code=400, detail="Creating the transaction failed")

    response = {
        "message": "Transaction added successfully",
        "transaction": {
            "sender": wallet.public_key,
            "recipient": transaction.recipient,
            "amount": transaction.amount,
        },
        "funds": blockchain.get_balance(),
    }
    return JSONResponse(content=response, status_code=201)


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
        raise HTTPException(status_code=400, detail="Adding a block failed")


@app.get("/transaction")
async def get_transaction():
    transactions = blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return JSONResponse(content=dict_transactions, status_code=200)


@app.get("/chain")
async def get_chain():
    chain_snapshot = blockchain.get_chain()
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]

    if not dict_chain:
        raise HTTPException(status_code=404, detail="Empty chain")

    return JSONResponse(content=dict_chain, status_code=200)
