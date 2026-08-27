from dataclasses import dataclass

@dataclass
class Product:
    product_id: int
    product_name: str
    model_year: int

    def __hash__(self):
        return hash(self.product_id)

    def __eq__(self, other):
        return self.product_id == other.product_id

    def __str__(self):
        return f"{self.product_name} - {self.model_year}"