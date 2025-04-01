# Inactive Users per Equipment

This Python script identifies users who haven't used certain lab equipment in the past X months, based on a CSV export from a booking system (e.g., Agendo).
The input file is a report named  *Last user activity*.

## ⚙️ Features

- Interactive file selection via file picker.
- Filters by a predefined list of equipment.
- Ignores specific users (e.g. admins or staff).
- Detects inactive users (including those who never used the equipment).
- Displays users sorted by their last recorded activity.

## 🐍 Requirements

- Python 3.x
- `pandas`
- `tkinter` (usually comes bundled with Python)

To install the required package:

```bash
pip install pandas
