from fastapi import FastAPI, Response
from pydantic import BaseModel
import random
import string
import httpx

app = FastAPI(title="Denim Co. Discount API")

TRACKING_PIXEL = bytes.fromhex(
    "47494638396101000100800000000000ffffff21f90401000000002c00000000010001000002024401003b"
)

OPENED_WEBHOOK_URL = "https://hook.eu1.make.com/dxxy7mvsspbwrmu31y3unn5h1lm3g9ex"

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

@app.get("/track-open/{email}")
def track_open(email: str):
    # Fire-and-forget notification to Make that this email was opened.
    # If this fails (e.g. Make webhook down), we still return the pixel
    # so the email itself never looks broken to the customer.
    try:
        httpx.post(OPENED_WEBHOOK_URL, json={"email": email}, headers={"x-make-apikey": "atupcy-order-secret-2026"}, timeout=3)

    except Exception:
        pass
    return Response(content=TRACKING_PIXEL, media_type="image/gif")