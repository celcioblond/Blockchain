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
    response = {"all_nodes": nodes}
    return JSONResponse(content=response, status_code=status.HTTP_200_OK)


@router.delete("/node/{node_url}", status_code=status.HTTP_200_OK)
async def remove_node(node_url: str):
    if node_url == "" or node_url == None:
        raise HTTPException(status_code=400, detail="Node not found")
    state.blockchain.remove_peer_node(node_url)
    message = "Node removed correctly"
    return JSONResponse(content=message)
