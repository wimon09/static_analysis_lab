from src.invoice_service import InvoiceService, Invoice, LineItem

def test_compute_total_basic_th():
    service = InvoiceService()
    inv = Invoice(
        invoice_id="INV001",
        customer_id="C001",
        country="TH",
        membership="none",
        coupon=None,
        items=[
            LineItem(sku="B001", category="book", unit_price=100, qty=2)
        ]
    )

    total, warnings = service.compute_total(inv)

    assert total > 0
    assert warnings == []

def test_compute_total_with_coupon():
    service = InvoiceService()
    inv = Invoice(
        invoice_id="INV002",
        customer_id="C002",
        country="US",
        membership="gold",
        coupon="WELCOME10",
        items=[
            LineItem(sku="E001", category="electronics", unit_price=500, qty=1)
        ]
    )

    total, _ = service.compute_total(inv)

    assert total > 0

