# Workbook Specification

## Workbook Purpose

The workbook is the membership payment register. It stores member payment dates by month.

## Worksheets

Worksheets are named by year. Examples include:

- `2026`
- `2025`
- `2024`

Additional worksheets may exist, including:

- `Archive`
- `Sheet1`
- `Sheet2`

The application must determine the working worksheet automatically.

## Worksheet Layout

The header row is row `1`.

Member data starts at row `2`.

## Columns

| Columns | Meaning |
| --- | --- |
| A | Sequential number |
| B | Member full name |
| C | MAC address |
| D-O | Monthly payment columns |

The headers for columns D-O are Excel dates in the form `01.01.YYYY` through `01.12.YYYY`:

- `01.01.YYYY`
- `01.02.YYYY`
- ...
- `01.12.YYYY`

## Payment Cells

Each payment cell contains either:

- a payment date, or
- an empty value

The application must never replace formulas.

## Member Identification

The primary key is the MAC address in column C.

Future versions may support:

- multiple MAC addresses
- member name lookup

## Workbook Safety

The application must preserve:

- formatting
- formulas
- merged cells
- comments
- validation
- hidden rows and columns

Only payment cells may change during a future write workflow.

## Import Principle

The import flow is:

```text
Bank statement
		|
	Payment
		|
	Member
		|
	 Month
		|
Write payment date
```

No other cells may be modified.

## Workbook Assumptions

- The workbook contains at least one year-named worksheet.
- The application selects the working year worksheet automatically.
- Member headers are on row 1.
- Member data begins on row 2.
- Column C contains the permanent MAC identifier.
- Columns D-O contain January through December payment cells.
- Month headers are Excel date values representing the first day of each month.
- Payment cell values are dates or empty values.
- Existing formulas, formatting, merged cells, comments, validation, and hidden rows or columns are part of the workbook contract.
- The original workbook must never be overwritten.
