from decimal import Decimal
from pydantic import BaseModel, ConfigDict

class NormalizedTransaction(BaseModel):
    model_config = ConfigDict(extra="forbid")
    id: int
    amount: Decimal
    currency: str | None = None
    transactionDate: str | None = None
    status: str = "UNKNOWN"
    originalReference: str | None = None
    concept: str | None = None
