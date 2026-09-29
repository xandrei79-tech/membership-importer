from datetime import date
from decimal import Decimal
from pathlib import Path

from openpyxl import Workbook

from membership_importer.models.payment import Payment
from membership_importer.services.payment_parser import PaymentParser


def test_payment_parser_reads_multiple_statements_and_returns_payment_objects(
    tmp_path: Path,
) -> None:
    csv_path = tmp_path / "statement.csv"
    csv_path.write_text(
        "date,amount,payer,description\n"
        "2026-08-27,10.50,Jane Doe,Membership fee\n"
        "27.08.2026,-7.00,John Smith,Donation\n",
        encoding="utf-8",
    )

    workbook_path = tmp_path / "second.xlsx"
    workbook = Workbook()
    sheet = workbook.active
    sheet.append(["payment_date", "amount", "payer_name", "description"])
    sheet.append(["2026-09-01", "25.00", " Anna  Brown ", "Annual renewal"])
    workbook.save(workbook_path)

    parser = PaymentParser()
    payments = parser.parse_statements((csv_path, workbook_path))

    assert len(payments) == 3
    assert all(isinstance(payment, Payment) for payment in payments)
    assert payments[0].payment_date == date(2026, 8, 27)
    assert payments[0].amount == Decimal("10.50")
    assert payments[0].payer_name == "Jane Doe"
    assert payments[0].description == "Membership fee"
    assert payments[1].amount == Decimal("7.00")
    assert payments[2].payer_name == "Anna Brown"
    assert payments[2].description == "Annual renewal"


def test_payment_parser_normalizes_single_statement_file() -> None:
    parser = PaymentParser()

    payment = parser.parse_statement(
        {
            "date": "2026/08/28",
            "payer": "  Test Member  ",
            "amount": " 12.34 ",
            "description": "  Membership payment  ",
        }
    )

    assert len(payment) == 1
    assert payment[0].payment_date == date(2026, 8, 28)
    assert payment[0].payer_name == "Test Member"
    assert payment[0].amount == Decimal("12.34")
    assert payment[0].description == "Membership payment"
