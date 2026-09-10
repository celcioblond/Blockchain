from pydantic import BaseModel


class BlockTransaction(BaseModel):
    sender: str
    recipient: str
    amount: float
    signature: str


class Block(BaseModel):
    index: int
    previous_hash: str
    timestamp: float
    transactions: list[BlockTransaction]
    proof: int


class BroadcastBlockRequest(BaseModel):
    block: Block
