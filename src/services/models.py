from pydantic import BaseModel
from uuid import UUID


class AddProduct(BaseModel):
    name: str
    pricePerUnit: int
    productDetails: str
    quantityInstock: int

class ProductAddedResponse(AddProduct):
    id: UUID

    class Config:
        from_attributes=True


class SaleMake(BaseModel):
    quantity_sold: int
    customer_name: str
    customer_number: str
    amount: int

    product_id: UUID
    admin_id: UUID


class Supplier(BaseModel):
    firstname: str
    lastname: str
    phone: str
    email: str


class PurchaseMake(BaseModel):
    quantity: int
    amount: int

    supplier_id: UUID
    product_id: UUID
    admin_id: UUID
