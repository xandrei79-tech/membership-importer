# Configuration Workbooks

This directory contains the spreadsheets used to configure membership payment processing. Each workbook is a template with headers only. Add real configuration records only when the corresponding feature is implemented and its format is confirmed.

## `payment_groups.xlsx`

Defines payment groups and the payment rules associated with each group.

Headers:

- `group_name`
- `description`
- `monthly_amount`
- `currency`

## `aliases.xlsx`

Maps alternate names found in imported payment data to a canonical member or payer name.

Headers:

- `alias`
- `canonical_name`

## `tariffs.xlsx`

Defines membership tariff amounts over time. Effective dates allow future tariff changes without rewriting historical configuration.

Headers:

- `effective_from`
- `monthly_amount`
- `currency`

## General Notes

- These workbooks contain headers only and intentionally contain no sample data.
- Header names are part of the configuration contract and should not be changed casually.
- Configuration changes must not modify the original membership workbook.
- Dates should use an unambiguous Excel date value when records are added.
- Monetary amounts should use decimal currency values.
