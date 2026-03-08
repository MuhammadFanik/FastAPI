# Product Inventory

# Create a Product model with these fields:
# product_name → text
# price → decimal number
# stock → whole number
# discount → decimal number
# is_available → True/False
# secret_cost → decimal number (internal cost, should never be shared!)


from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

product_info = {
    "product_name": "Laptop",
    "price": 999.99,
    "stock": 50,
    "discount": 10.0,
    "is_available": True,
    "secret_cost": 500.0
}

class Product(BaseModel):
    product_name: str
    price: float
    stock: int
    discount: float
    is_available: bool
    secret_cost: float

    @computed_field
    @property
    def discounted_price(self) -> float:
        discounted_price =  self.price - (self.price * (self.discount/100))
        return discounted_price

prod1 = Product(**product_info)

full_dict = prod1.model_dump()
print(full_dict)

full_dict2 = prod1.model_dump(exclude={"secret_cost"})
print(full_dict2)

full_dict3 = prod1.model_dump(include={"product_name", "discounted_price"})
print(full_dict3)

as_json = prod1.model_dump_json()
print(as_json)