from pathlib import Path

from openpyxl import Workbook

from membership_importer.services.customer_repository import CustomerRepository


def test_repository_loads_customers_and_groups(tmp_path: Path) -> None:
    workbook_path = tmp_path / "customers.xlsx"
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.title = "Customers"
    worksheet.append([
        "customer_id",
        "customer_name",
        "group_name",
        "description",
        "monthly_amount",
        "currency",
        "mac",
        "full_name",
        "active",
    ])
    worksheet.append([
        "CUST-01",
        "Alice Example",
        "Gold",
        "Premium members",
        15.00,
        "EUR",
        "AA:BB:CC:DD:EE:FF",
        "Alice Member",
        True,
    ])
    worksheet.append([
        "CUST-01",
        "Alice Example",
        "Gold",
        "Premium members",
        15.00,
        "EUR",
        "11:22:33:44:55:66",
        "Second Member",
        True,
    ])
    worksheet.append([
        "CUST-02",
        "Bob Example",
        "Silver",
        "Standard plan",
        10.00,
        "EUR",
        "77:88:99:AA:BB:CC",
        "Bob Member",
        True,
    ])
    workbook.save(workbook_path)

    repository = CustomerRepository(workbook_path)

    customer = repository.get_customer("CUST-01")
    assert customer is not None
    assert customer.customer_id == "CUST-01"
    assert len(customer.members) == 2

    member = repository.get_member("AA:BB:CC:DD:EE:FF")
    assert member is not None
    assert member.full_name == "Alice Member"

    group = repository.get_group("CUST-01")
    assert group is not None
    assert group.name == "Gold"

    groups = repository.list_groups()
    assert [group.name for group in groups] == ["Gold", "Silver"]


def test_repository_rejects_missing_required_columns(tmp_path: Path) -> None:
    workbook_path = tmp_path / "customers.xlsx"
    workbook = Workbook()
    worksheet = workbook.active
    worksheet.append(["customer_id", "customer_name", "mac"])
    worksheet.append(["CUST-01", "Alice Example", "AA:BB:CC:DD:EE:FF"])
    workbook.save(workbook_path)

    try:
        CustomerRepository(workbook_path)
    except ValueError as error:
        assert "group_name" in str(error)
    else:
        raise AssertionError("Missing required columns should raise ValueError")
