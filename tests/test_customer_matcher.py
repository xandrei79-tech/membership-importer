from datetime import date
from decimal import Decimal
from pathlib import Path

from openpyxl import Workbook

from membership_importer.models.payment import Payment
from membership_importer.services.customer_matcher import CustomerMatcher
from membership_importer.services.customer_repository import CustomerRepository


def _make_repository(path: Path, names: list[tuple[str, str]]) -> CustomerRepository:
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(
        [
            "customer_id",
            "customer_name",
            "group_name",
            "description",
            "monthly_amount",
            "currency",
            "mac",
            "full_name",
            "active",
        ]
    )
    for customer_id, customer_name in names:
        worksheet.append(
            [customer_id, customer_name, "", "", 0, "EUR", "", "", True]
        )
    workbook.save(path)
    return CustomerRepository(path)


def _payment(payer_name: str) -> Payment:
    return Payment(
        payment_date=date(2025, 1, 1),
        amount=Decimal("10.00"),
        payer_name=payer_name,
        description="Membership fee",
        reference_number=None,
        source_bank="Test bank",
        original_record={"payer_name": payer_name},
    )


def test_matcher_matches_case_insensitively_and_normalizes_whitespace(
    tmp_path: Path,
) -> None:
    repository = _make_repository(
        tmp_path / "customers.xlsx", [("CUST-01", "Alice   Example")]
    )
    payment = _payment("  aLiCe\tExample  ")

    result = CustomerMatcher(repository, aliases={}).match(payment)

    assert result.status == "matched"
    assert result.customer is repository.get_customer("CUST-01")
    assert payment.payer_name == "  aLiCe\tExample  "
    assert result.customer is not None
    assert result.customer.members == []


def test_matcher_resolves_alias_to_canonical_customer(tmp_path: Path) -> None:
    repository = _make_repository(
        tmp_path / "customers.xlsx", [("CUST-01", "Alice Example")]
    )
    matcher = CustomerMatcher(
        repository,
        aliases={"A. Example": "Alice Example"},
    )

    result = matcher.match(_payment(" a.   example "))

    assert result.status == "matched"
    assert result.customer is repository.get_customer("CUST-01")


def test_matcher_returns_unmatched_for_unknown_payer(tmp_path: Path) -> None:
    repository = _make_repository(
        tmp_path / "customers.xlsx", [("CUST-01", "Alice Example")]
    )

    result = CustomerMatcher(repository, aliases={}).match(_payment("Unknown Payer"))

    assert result.status == "unmatched"
    assert result.customer is None
    assert result.candidates == ()


def test_matcher_returns_ambiguous_for_duplicate_customer_names(tmp_path: Path) -> None:
    repository = _make_repository(
        tmp_path / "customers.xlsx",
        [("CUST-01", "Alex Example"), ("CUST-02", " alex   example ")],
    )

    result = CustomerMatcher(repository, aliases={}).match(_payment("Alex Example"))

    assert result.status == "ambiguous"
    assert result.customer is None
    assert [customer.customer_id for customer in result.candidates] == [
        "CUST-01",
        "CUST-02",
    ]


def test_matcher_loads_aliases_from_workbook(tmp_path: Path) -> None:
    repository = _make_repository(
        tmp_path / "customers.xlsx", [("CUST-01", "Alice Example")]
    )
    aliases_path = tmp_path / "aliases.xlsx"
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(["alias", "canonical_name"])
    worksheet.append(["A. Example", "Alice Example"])
    workbook.save(aliases_path)

    result = CustomerMatcher(repository, aliases_path=aliases_path).match(
        _payment("A. Example")
    )

    assert result.status == "matched"
    assert result.customer is repository.get_customer("CUST-01")
