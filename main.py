from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from core.config import CORS_ORIGINS
from routers import chain, mine, node, transactions, wallet

app = FastAPI()

app.add_middleware(
    CORSMiddleware,
    allow_origins=CORS_ORIGINS,
    allow_methods=["*"],
    allow_headers=["*"],
    allow_credentials=True,
)

app.include_router(wallet.router)
app.include_router(transactions.router)
app.include_router(mine.router)
app.include_router(chain.router)
app.include_router(node.router)

if __name__ == "__main__":
    import os
    from argparse import ArgumentParser

    import uvicorn

    parser = ArgumentParser()
    parser.add_argument("-p", "--port", type=int, default=5000)
    args = parser.parse_args()
    port = args.port

    # core.state reads NODE_ID when it is imported, so it must be set before
    # uvicorn imports the app (and it is inherited by the reloader subprocess).
    os.environ["NODE_ID"] = str(port)

    uvicorn.run("main:app", host="0.0.0.0", port=port, reload=True)
