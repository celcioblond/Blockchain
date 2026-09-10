from pydantic import BaseModel, Field


class BroadcastTransactionRequest(BaseModel):
    sender: str = Field(min_length=3)
    recipient: str = Field(min_length=3)
    amount: float = Field(gt=0)
    signature: str = Field(min_length=3)
