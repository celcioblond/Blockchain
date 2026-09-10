from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from core import state
from schemas.broadcast_transaction_request import BroadcastTransactionRequest
from schemas.transaction_request import TransactionRequest

router = APIRouter()


@router.post("/transaction", status_code=status.HTTP_201_CREATED)
def add_transaction(transaction: TransactionRequest):
    if state.wallet.public_key is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="No wallet set up"
        )

    signature = state.wallet.sign_transaction(
        state.wallet.public_key, transaction.recipient, transaction.amount
    )
    success = state.blockchain.add_transaction(
        transaction.recipient, state.wallet.public_key, signature, transaction.amount
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Creating the transaction failed",
        )

    response = {
        "message": "Transaction added successfully",
        "transaction": {
            "sender": state.wallet.public_key,
            "recipient": transaction.recipient,
            "amount": transaction.amount,
        },
        "funds": state.blockchain.get_balance(),
    }
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)


@router.get("/transaction", status_code=status.HTTP_200_OK)
async def get_transaction():
    transactions = state.blockchain.get_open_transactions()
    dict_transactions = [tx.__dict__ for tx in transactions]
    return JSONResponse(content=dict_transactions, status_code=status.HTTP_200_OK)


@router.post("/broadcast-transaction", status_code=status.HTTP_201_CREATED)
async def broadcast_transaction(transaction: BroadcastTransactionRequest):
    success = state.blockchain.add_transaction(
        transaction.recipient,
        transaction.sender,
        transaction.signature,
        transaction.amount,
        is_receiving=True,
    )

    if not success:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Creating the transaction failed",
        )

    response = {
        "message": "Successfully added transaction",
        "transaction": {
            "sender": transaction.sender,
            "recipient": transaction.recipient,
            "amount": transaction.amount,
            "signature": transaction.signature,
        },
    }
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
