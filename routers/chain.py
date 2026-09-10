from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from core import state

router = APIRouter()


@router.get("/chain", status_code=status.HTTP_200_OK)
async def get_chain():
    chain_snapshot = state.blockchain.get_chain()
    dict_chain = [block.__dict__.copy() for block in chain_snapshot]
    for dict_block in dict_chain:
        dict_block["transactions"] = [tx.__dict__ for tx in dict_block["transactions"]]

    if not dict_chain:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Empty chain")

    return JSONResponse(content=dict_chain, status_code=status.HTTP_200_OK)


@router.post("/resolve-conflicts", status_code=status.HTTP_201_CREATED)
def resolve_conflicts():
    replaced = state.blockchain.resolve()
    if replaced:
        return JSONResponse(
            content="Chain replaced", status_code=status.HTTP_201_CREATED
        )
    else:
        return JSONResponse(content="Local chain kept", status_code=status.HTTP_200_OK)
