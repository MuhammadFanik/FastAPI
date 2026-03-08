# ONLINE ORDER SYSTEM

# Create an Order model with these fields:
# customer_name → text
# product → text
# price_per_unit → decimal number
# quantity → whole number
# discount → decimal number (percentage e.g. 10 means 10%)


from pydantic import BaseModel, EmailStr, computed_field
from typing import List, Dict

order_info = {
    "customer_name": "Alex",
    "product": "Laptop",
    "price_per_unit": 800.0,
    "quantity": 3,
    "discount": 10.0
}

class Order(BaseModel):
    customer_name: str
    product: str
    price_per_unit: float
    quantity: int
    discount: float

    # Computed Field to calculate the total price
    @computed_field
    @property
    def total_price(self) -> float:
        total_price = self.price_per_unit * self.quantity
        return total_price


    # Computed Field to calculate the discounted price
    @computed_field
    @property
    def discounted_price(self) -> float:
        total_price = self.price_per_unit * self.quantity
        discounted_price = total_price - (total_price * (self.discount/100))
        return discounted_price

def print_details(customer:Order):
    print(f"Customer Name: {customer.customer_name}")
    print(f"Product: {customer.product}")
    print(f"Price per unit: {customer.price_per_unit}")
    print(f"Quantity: {customer.quantity}")
    print(f"Total Price: {customer.total_price}")
    print(f"Price after discount: {customer.discounted_price}")


order1 = Order(**order_info)
print_details(order1)