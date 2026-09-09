from fastapi import APIRouter, HTTPException, status
from fastapi.responses import JSONResponse

from core import state
from schemas.node_request import NodeRequest

router = APIRouter()


@router.post("/node", status_code=status.HTTP_201_CREATED)
async def add_node(node: NodeRequest):
    if not node:
        raise HTTPException(status_code=400, detail="No data attached")

    state.blockchain.add_peer_node(node.node)

    response = {
        "message": "Node added successfully",
        "all_nodes": state.blockchain.get_peer_nodes(),
    }
    return JSONResponse(content=response, status_code=status.HTTP_201_CREATED)


@router.get("/node", status_code=status.HTTP_200_OK)
async def get_nodes():
    nodes = state.blockchain.get_peer_nodes()
    return JSONResponse(content=nodes, status_code=status.HTTP_200_OK)
