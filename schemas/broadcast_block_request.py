from pydantic import BaseModel


class BlockTransaction(BaseModel):
    sender: str
    recipient: str
    # int | float keeps the original type (e.g. MINING_REWARD = 10), so the
    # block hashes the same on every node.
    amount: int | float
    signature: str


class Block(BaseModel):
    index: int
    previous_hash: str
    timestamp: float
    transactions: list[BlockTransaction]
    proof: int


class BroadcastBlockRequest(BaseModel):
    block: Block
