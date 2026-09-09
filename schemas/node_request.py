from pydantic import BaseModel, Field


class NodeRequest(BaseModel):
    node: str = Field(min_length=5)
