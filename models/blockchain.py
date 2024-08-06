from typing import Optional

from pydantic import BaseModel, field_validator


class Asset(BaseModel):
    contract_address: str
    balance: str
    quote: Optional[float] = None
    symbol: Optional[str] = None

    @field_validator('quote', mode='before')
    def validate_quote(cls, v):
        if v is None or v == "":
            return 0.0
        try:
            return float(v)
        except ValueError:
            raise ValueError("quote should be a valid number")

    @field_validator('symbol', mode='before')
    def validate_symbol(cls, v):
        if v is None or v == "":
            return "N/A"
        if not isinstance(v, str):
            raise ValueError("symbol should be a valid string")
        return v


class Transaction(BaseModel):
    block_signed_at: str
    tx_hash: str
    from_address: str
    to_address: str
    value: str
    gas_spent: str
    gas_price: str
