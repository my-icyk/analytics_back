from app.repositories.base import BaseRepository


class SpecificRepository(BaseRepository):
    def exec_price_for_nomen_for_api(self, product_code: str):
        sql = """
           select * from testing_db.functions.GetProductSummaryByCode(:product_code)
        """

        rows = self._fetch_all(sql, {"product_code": product_code})
        return rows
