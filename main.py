from fastapi import FastAPI
from pydantic import BaseModel
import random
import string

app = FastAPI(title="Denim Co. Discount API")


class CartRequest(BaseModel):
    customerName: str
    cartValue: float
    email: str


def generate_code(prefix: str) -> str:
    suffix = "".join(random.choices(string.ascii_uppercase + string.digits, k=6))
    return f"{prefix}-{suffix}"


@app.get("/")
def root():
    return {"status": "ok", "service": "Denim Co. Discount API"}


@app.post("/generate-discount")
def generate_discount(cart: CartRequest):
    if cart.cartValue < 50:
        percent = 10
        tier = "standard"
        prefix = "DENIM10"
    elif cart.cartValue < 150:
        percent = 15
        tier = "mid"
        prefix = "DENIM15"
    else:
        percent = 20
        tier = "vip"
        prefix = "DENIM20"

    code = generate_code(prefix)

    return {
        "discountCode": code,
        "discountPercent": percent,
        "tier": tier
    }