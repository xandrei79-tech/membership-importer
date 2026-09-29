# Business Rules

## Purpose

This document contains all business rules used by the Membership Importer.

The application must always follow these rules exactly.

If a situation is not described here, the application must stop automatic processing and request manual confirmation.

---

# Membership fee

The standard membership fee is:

10 EUR per month

---

# Payment allocation

Payments are allocated chronologically.

Example:

Payment:
50 EUR

Result:

January   10 EUR
February  10 EUR
March     10 EUR
April     10 EUR
May       10 EUR

---

# Overpayment

Unused money is never lost.

The remaining balance is automatically transferred to future months.

---

# Partial payment

If the payment is less than one monthly fee, the application must not invent missing payments.

The payment is stored exactly as received.

---

# Original workbook

The original Excel workbook is never modified.

Before every import:

- create backup
- work on a copy

---

# Workbook formatting

The application must preserve:

- colours
- borders
- formulas
- merged cells
- fonts
- widths
- comments

No formatting changes are allowed.

---

# Member identification

Every member has a permanent identifier.

Current identifier:

MAC

The MAC identifier never changes automatically.

---

# Unknown payment

If a payment cannot be matched:

- do not assign automatically
- add it to the review list
- require manual confirmation

---

# Import log

Every import creates a log.

The log contains:

- import date
- source file
- workbook
- matched payments
- unmatched payments
- warnings
- errors

---

# Safety

Automatic processing must never destroy data.

If there is uncertainty:

STOP

Ask the user.