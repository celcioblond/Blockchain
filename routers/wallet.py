from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from core import state
from models.blockchain import Blockchain

router = APIRouter()


@router.post("/wallet", status_code=status.HTTP_201_CREATED)
async def create_keys():
    state.wallet.create_keys()
    if state.wallet.save_keys():
        state.blockchain = Blockchain(state.wallet.public_key, state.NODE_ID)
        response = {
            "public_key": state.wallet.public_key,
            "private_key": state.wallet.private_key,
            "funds": state.blockchain.get_balance(),
        }
        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Saving the key failed"
        )


@router.get("/wallet", status_code=status.HTTP_200_OK)
async def load_keys():
    if not state.wallet.load_keys():
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail="Loading the keys failed",
        )

    state.blockchain = Blockchain(state.wallet.public_key, state.NODE_ID)

    return JSONResponse(
        content={
            "public_key": state.wallet.public_key,
            "private_key": state.wallet.private_key,
            "funds": state.blockchain.get_balance(),
        },
        status_code=status.HTTP_200_OK,
    )


@router.get("/balance", status_code=status.HTTP_200_OK)
async def get_balance():
    balance = state.blockchain.get_balance()
    if balance != None:
        response = {
            "message": "Fetched balance succesfully",
            "balance": balance,
        }
        return JSONResponse(content=response, status_code=status.HTTP_200_OK)
    else:
        raise HTTPException(
            status_code=status.HTTP_500_INTERNAL_SERVER_ERROR,
            detail={
                "message": "Loading balance failed",
                "wallet_set_up": state.wallet.public_key != None,
            },
        )
