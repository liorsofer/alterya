import random
from typing import List, Optional

import httpx
from fastapi import HTTPException, APIRouter

from models.blockchain import Asset, Transaction

router = APIRouter(tags=["Blockchain"])

COVALENT_API_KEYS = [
    "cqt_wFDJ6q9g4BRGdjGBqjdgjy7D4BtF",
    "cqt_wFb4xHHk7pPXKcVgjpC6BW3hrwqB",
    "cqt_wFXJD7dDmyd34RdY66Y8BgPYdcmY",
    "cqt_wFTbVdbjbfTRBPCP3DdmpxhKt7MM",
    "cqt_wFxfkxyCkBYwxWTdcqpqCvRtBWgV",
]

BASE_URL = "https://api.covalenthq.com/v1"


# I didn't you the "from covalent import CovalentClient" as provided in their
# documentation as i assumed it was just made for showing the example online
async def fetch_covalent_data(endpoint: str, params: Optional[dict] = None):
    url = f"{BASE_URL}{endpoint}"
    api_key = random.choice(COVALENT_API_KEYS)
    headers = {"Authorization": f"Bearer {api_key}"}
    async with httpx.AsyncClient() as client:
        response = await client.get(url, headers=headers, params=params)
        response.raise_for_status()
        return response.json()


@router.get("/wallet/{address}/assets", response_model=List[Asset])
async def get_wallet_assets(address: str, chain_id: int = 1):
    try:
        data = await fetch_covalent_data(f"/{chain_id}/address/{address}/balances_v2/")
        return [
            Asset(
                contract_address=item["contract_address"],
                balance=item["balance"],
                quote=item.get("quote", 0.0) if item.get("quote") is not None else 0.0,
                symbol=item.get("contract_ticker_symbol", "N/A"),
            )
            for item in data["data"]["items"]
        ]
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/wallet/{address}/total_value")
async def get_wallet_total_value(address: str, chain_id: int = 1):
    try:
        data = await fetch_covalent_data(f"/{chain_id}/address/{address}/balances_v2/")
        total_value = sum(
            item.get("quote", 0.0) if item.get("quote") is not None else 0.0 for item in data["data"]["items"])
        return {"total_value_usd": total_value}
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))


@router.get("/wallet/{address}/transactions", response_model=List[Transaction])
async def get_wallet_transactions(
        address: str, chain_id: str, page: int = 0, page_size: int = 10
):
    try:
        data = await fetch_covalent_data(f"/{chain_id}/address/{address}/transactions_v3/page/{page}/",
                                         {"page-size": page_size})
        return [
            Transaction(
                block_signed_at=item["block_signed_at"],
                tx_hash=item["tx_hash"],
                from_address=item["from_address"],
                to_address=item["to_address"],
                value=item["value"],
                gas_spent=str(item["gas_spent"]),
                gas_price=str(item["gas_price"]),
            )
            for item in data["data"]["items"]
        ]
    except httpx.HTTPStatusError as e:
        raise HTTPException(status_code=e.response.status_code, detail=str(e))
