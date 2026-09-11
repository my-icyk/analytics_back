from app.domains.specific_models import PriceSummary, ProductSummary
from app.exceptions.exceptions import NotFoundError
from app.repositories.specific_repository import SpecificRepository


class SpecificService:
    def __init__(self, specific_repository: SpecificRepository):
        self.specific_repository = specific_repository

    def exec_price_for_nomen_for_api(self, product_code: str) -> ProductSummary:

        rows = self.specific_repository.exec_price_for_nomen_for_api(product_code)

        if not rows:
            raise NotFoundError("PriceSummary", "product_code:", product_code)

        product = ProductSummary(
            product_code=rows[0]["product_code"],
            product_name=rows[0]["product_name"],
            prices=[
                PriceSummary(
                    warehouse_name=row["warehouse_name"],
                    quantity=row["quantity"],
                    unit_cost=row["unit_cost"],
                    price_s=row["price_s"],
                    price_ultra=row["price_ultra"],
                    price_enter=row["price_enter"],
                )
                for row in rows
            ],
        )

        return product
