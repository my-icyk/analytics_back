from pydantic import BaseModel


class PriceSummary(BaseModel):
    warehouse_name: str
    quantity: int
    unit_cost: float
    price_s: float
    price_ultra: float
    price_enter: float


class ProductSummary(BaseModel):
    product_code: str
    product_name: str
    prices: list[PriceSummary]
