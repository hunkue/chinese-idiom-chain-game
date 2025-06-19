# Chinese Idiom Chain Game

![Python version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Repo size](https://img.shields.io/github/repo-size/hunkue/chinese-idiom-chain-game)
![Last commit](https://img.shields.io/github/last-commit/hunkue/chinese-idiom-chain-game)
![Issues](https://img.shields.io/github/issues/hunkue/chinese-idiom-chain-game)

This is a Python-based **Chinese idiom chain game** supporting both Command Line Interface (CLI) and Graphical User Interface (GUI using `tkinter`).  
It integrates with a MySQL database to retrieve idioms and store player records.  
The project now uses [`uv`](https://github.com/astral-sh/uv) for dependency and environment management.

Future plan: deployment to a personal website via Django — [hunkue.com](https://hunkue.com)

---

## 📁 Project Structure

```
chinese-idiom-chain-game/
├── idiom_chain.py             # Main GUI entry point
├── main.py                    # CLI entry point
├── game.py                    # Core game logic
├── game_timer.py              # Countdown timer module
├── game_manager.py            # Game session controller
├── records_database.py        # Handles player score records
├── idiom_database.py          # Handles idiom data from database
├── first-time-execute/        # One-time setup scripts
│   ├── change_csv_header.py   # Adjusts CSV headers to expected format
│   ├── data_test.py           # Data validation/testing
│   ├── import_data.py         # Imports idiom data into DB
│   └── record_data.py         # Inserts sample score records
├── previous-test-version/     # Legacy or experimental game interfaces
│   ├── idiom_solitaire_origin.py
│   ├── idiom_solitaire_async.py
│   ├── idiom_solitaire_sync.py
│   ├── idiom_solitaire_async_success.py
│   └── idiom_solitaire_select.py
├── pyproject.toml             # uv dependency and project config
├── uv.lock                    # Lockfile for uv dependencies
├── .env                       # Local environment variables (ignored)
├── LICENSE                    # MIT license
├── README.md                  # Project documentation
└── ...
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hunkue/chinese-idiom-chain-game.git
cd chinese-idiom-chain-game
```

### 2. Install System Dependencies (macOS example)

```bash
brew install mysql pkg-config
```

> For other platforms, please refer to the [official MySQL installation guide](https://dev.mysql.com/doc/).


---

### 3. Set Up Environment with `uv`

```bash
uv sync
source .venv/bin/activate
```

This installs all dependencies and activates the virtual environment.  
You can inspect or modify dependencies in `pyproject.toml`.


---

### 4. Setup `.env` File

Create a `.env` file in the project root to store your environment variables.  
**DO NOT commit this file to version control.**

Example:

```env
DB_HOST=localhost
DB_USER=root
DB_PASSWORD=your_password_here
DB_NAME=game_db
```

---

### 5. Prepare Initial Idiom Data (One-time Setup)

Before running the game, you must initialize the database and import idioms.

Please download the latest idiom dataset manually from Taiwan Ministry of Education:  
🔗 https://language.moe.gov.tw/001/Upload/Files/site_content/M0001/respub/dict_idiomsdict_download.html

The downloaded `.csv` file is **not included** (intentionally `.gitignore`) to ensure users always fetch the latest version.

Then run the initialization scripts located in `first-time-execute/`.  
*(Confirm these match your repo content. Adjust names if needed.)*


---

### 6. Run the Application

#### GUI version

```bash
uv run idiom_chain.py
```

#### CLI version (if available)

```bash
uv run main.py
```

---

## ✨ Features

- 🧠 Automatic idiom prompts and answer validation
- ⏱️ 30-second countdown timer
- 💾 MySQL-based idiom and score persistence
- 🎨 GUI built with `tkinter`  
- 🚨 **Rescue request:** spend 3 points to get a “help” hint (feature still in development)  
- 🌐 Future Django web version in progress

---

## 🧭 Roadmap

| Feature                            | Status           |
|------------------------------------|------------------|
| GUI with tkinter                   | ✅ Completed      |
| CLI version                        | ✅ Completed      |
| Rescue request (3 points → hint)   | 🚧 In Development |
| Django Web UI                      | 🚧 In Progress    |

---

## 🛠️ Development Environment

- Python 3.10+
- [`uv`](https://github.com/astral-sh/uv)
- MySQL 8.0+
- GUI: `tkinter`
- `.env` for configuration

---

## 🤝 Contributing

Issues and pull requests are welcome!  
Feel free to open an issue or reach out if you’d like to collaborate or suggest improvements.

---

## 📝 License

This project is licensed under the MIT License.  
See [LICENSE](./LICENSE) for more details.