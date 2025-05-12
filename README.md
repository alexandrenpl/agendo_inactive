# Inactive Users per Equipment

This Python application identifies users who haven't used specific lab equipment in the past X months, based on a CSV report from the Agendo booking system 'Last user activity'. It features a simple and interactive graphical interface, allowing quick analysis, editing of filters, and visualisation of results. There is also an executable in dist directory.

The input file should be a report named **Last user activity**, exported from Agendo.

## ⚙️ Features

- ✅ Select the CSV file via a file picker.
- ✅ Set the number of months to check for inactivity.
- ✅ Filter by a predefined (and editable) list of equipment.
- ✅ Exclude specific users (e.g. staff/admins) from the analysis.
- ✅ Detects users who haven't used the equipment recently, including those who never used it.


## 🖥️ Interface

Built using `tkinter` (cross-platform GUI included with Python).

## 🐍 Requirements

- Python 3.x
- `pandas` (install via pip)
- `tkinter` (usually bundled with Python)

To install the required package:

bash
pip install pandas

## ▶️ How to Run

bash
python agendo_inactive_exec.py


Then use the interface to:
1. Select the **Last user activity** CSV file.
2. Define the inactivity period (in months).
3. Choose which systems to include in the check.
4. Run the analysis and view the results.

## 📦 Build a Standalone Executable (Windows)

To generate a `.exe` from the script, you can use [PyInstaller](https://pyinstaller.org/):

1. Install PyInstaller:

```bash
pip install pyinstaller
```

2. Run the following command to create a standalone executable:

```bash
pyinstaller --onefile --windowed agendo_inactive.py
pyinstaller agendo_inactive.spec

```

- `--onefile`: bundles everything into a single `.exe`.
- `--windowed`: prevents a terminal window from opening (ideal for GUI apps).

3. The `.exe` file will be generated inside the `dist` folder.

> 💡 You can rename the `.exe` and share it — no Python installation required on other machines.

## 📂 Structure

The app keeps the equipment list and excluded names embedded in the code — ideal for building a standalone `.exe`.

## 🔄 To-do / Future

- Optional export of results to file.
- Persistence of user-edited lists between sessions.
- Option to import custom equipment/exclusion lists.
- API integration

## 🧪 Tested on

- Windows 10
- Python 3.10
- CSV exports from Agendo (IGC)

---

Made with ❤️ by [@alexandrenpl](https://github.com/alexandrenpl) and 🤖 ChatGPT
```
