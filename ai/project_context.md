# Project Context

## Project name

Membership Importer

## Purpose

Membership Importer is a desktop application for importing bank payment data into an existing Excel workbook containing membership records.

The goal is to automate the monthly update process while preserving the existing workbook layout and formatting.

## Users

Primary user:

- Andrei

The application is intended for personal and internal organisational use.

## Main workflow

1. Open the membership workbook.
2. Import one or more bank statements.
3. Match payments to members.
4. Apply business rules.
5. Update the workbook.
6. Produce an import log.
7. Save a new workbook.

## Source of truth

The Excel workbook is always the primary source of data.

SQLite is used only for cache, logs and application settings.

## Requirements

- Preserve workbook formatting.
- Never overwrite the original workbook.
- Always create a backup.
- Support dry-run mode.
- Support manual review before saving.
- Keep a detailed import log.

## Supported import sources

Initially:

- LHV
- Swedbank
- SEB

Additional importers can be added later.

## Current project stage

Version:

0.1.0

Status:

Foundation