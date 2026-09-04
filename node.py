from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from wallet import Wallet

app = FastAPI()
wallet = Wallet()

app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)


@app.get("/")
async def get_ui():
    return {"response": "Hello world"}
