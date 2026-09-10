from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from core import state
from schemas.broadcast_block_request import BroadcastBlockRequest

router = APIRouter()


@router.post("/mine", status_code=status.HTTP_201_CREATED)
async def mine():
    block = state.blockchain.mine_block()
    if block != None:
        dict_block = block.__dict__.copy()
        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]
        response = {
            "message": "Block added successfully",
            "block": dict_block,
            "funds": state.blockchain.get_balance(),
        }
        return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)
    else:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Adding a block failed"
        )


@router.post("/broadcast-block", status_code=status.HTTP_201_CREATED)
async def broadcast_block(request: BroadcastBlockRequest):
    block = request.block
    last_block = state.blockchain.get_chain()[-1]

    if block.index == last_block.index + 1:
        pass
    elif block.index > last_block.index:
        pass
