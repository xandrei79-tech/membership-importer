# Membership Importer

## Technical Specification

Version: 0.1

---

# 1. Goal

The application automates the monthly processing of membership payments from bank statements into the existing Excel workbook.

The application must reduce manual work while preserving the current workflow.

---

# 2. Supported operating systems

- Windows 10
- Windows 11

---

# 3. User Interface

The application is a desktop application.

Main window contains:

- Open Workbook
- Import Bank Statement
- Preview
- Import
- Settings
- Logs
- Exit

---

# 4. Supported files

Membership workbook

- XLSX

Bank statements

- XLSX
- CSV
- XML (future)

---

# 5. Workflow

Step 1

Open workbook

↓

Step 2

Create backup

↓

Step 3

Import bank statement

↓

Step 4

Match members

↓

Step 5

Show preview

↓

Step 6

Manual review if required

↓

Step 7

Update workbook

↓

Step 8

Save new workbook

↓

Step 9

Generate log

---

# 6. Error handling

The application never silently ignores errors.

Every error is written into the import log.

Unknown payments require manual confirmation.

---

# 7. Safety

The original workbook is never modified.

Every import creates:

- backup
- log
- new workbook

---

# 8. Performance target

Workbook:

up to 5 000 members

Import time:

less than 10 seconds

---

# 9. Version 0.1

Functions:

- open workbook
- import payments
- payment matching
- update workbook
- backup
- log

---

# 10. Future versions

0.2

- automatic member search
- duplicate detection
- improved reports

0.3

- SQLite database
- statistics
- payment history

1.0

- full desktop application
- installer
- automatic updates