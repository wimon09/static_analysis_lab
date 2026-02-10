from dataclasses import dataclass
from typing import List, Optional, Dict, Tuple

@dataclass
class LineItem:
    sku: str
    category: str
    unit_price: float
    qty: int
    fragile: bool = False

@dataclass
class Invoice:
    invoice_id: str
    customer_id: str
    country: str
    membership: str
    coupon: Optional[str]
    items: List[LineItem]

class InvoiceService:
    def __init__(self) -> None:
        self._coupon_rate: Dict[str, float] = {
            "WELCOME10": 0.10,
            "VIP20": 0.20,
            "STUDENT5": 0.05
        }

    def _validate(self, inv: Invoice) -> List[str]:
        problems: List[str] = []
        if inv is None:
            problems.append("Invoice is missing")
            return problems
        if not inv.invoice_id:
            problems.append("Missing invoice_id")
        if not inv.customer_id:
            problems.append("Missing customer_id")
        if not inv.items:
            problems.append("Invoice must contain items")
        for it in inv.items:
            if not it.sku:
                problems.append("Item sku is missing")
            if it.qty <= 0:
                problems.append(f"Invalid qty for {it.sku}")
            if it.unit_price < 0:
                problems.append(f"Invalid price for {it.sku}")
            if it.category not in ("book", "food", "electronics", "other"):
                problems.append(f"Unknown category for {it.sku}")
        return problems

    def _calculate_shipping(self, country: str, subtotal: float) -> float:
        if country == "TH":
            return 60 if subtotal < 500 else 0
        elif country == "JP":
            return 600 if subtotal < 4000 else 0
        elif country == "US":
            if subtotal < 100:
                return 15
            elif subtotal < 300:
                return 8
            else:
                return 0
        else:
            return 25 if subtotal < 200 else 0

    def _calculate_discount(self, membership: str, subtotal: float, coupon: Optional[str], warnings: List[str]) -> float:
        discount = 0.0
        if membership == "gold":
            discount += subtotal * 0.03
        elif membership == "platinum":
            discount += subtotal * 0.05
        else:
            if subtotal > 3000:
                discount += 20

        if coupon is not None and coupon.strip() != "":
            code = coupon.strip()
            if code in self._coupon_rate:
                discount += subtotal * self._coupon_rate[code]
            else:
                warnings.append("Unknown coupon")

        return discount

    def _calculate_tax(self, country: str, subtotal: float, discount: float) -> float:
        if country == "TH":
            return (subtotal - discount) * 0.07
        elif country == "JP":
            return (subtotal - discount) * 0.10
        elif country == "US":
            return (subtotal - discount) * 0.08
        else:
            return (subtotal - discount) * 0.05

    def compute_total(self, inv: Invoice) -> Tuple[float, List[str]]:
        warnings: List[str] = []
        problems = self._validate(inv)
        if problems:
            raise ValueError("; ".join(problems))

        subtotal = 0.0
        fragile_fee = 0.0
        for it in inv.items:
            line = it.unit_price * it.qty
            subtotal += line
            if it.fragile:
                fragile_fee += 5.0 * it.qty

        shipping = self._calculate_shipping(inv.country, subtotal)
        discount = self._calculate_discount(inv.membership, subtotal, inv.coupon, warnings)
        tax = self._calculate_tax(inv.country, subtotal, discount)

        total = subtotal + shipping + fragile_fee + tax - discount
        if total < 0:
            total = 0

        if subtotal > 10000 and inv.membership not in ("gold", "platinum"):
            warnings.append("Consider membership upgrade")

        return total, warnings
