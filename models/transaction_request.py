from pydantic import BaseModel, Field


class TransactionRequest(BaseModel):
    recipient: str = Field(min_length=3)
    amount: float = Field(gt=0)
