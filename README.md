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
├── idiom_chain.py             # Main GUI program
├── game.py                    # Core game logic
├── game_timer.py              # Countdown timer module
├── records_database.py        # Game record database handler
├── idiom_database.py          # Idiom database loader
├── pyproject.toml             # uv-managed project configuration
├── .env                       # Environment variable configuration (DO NOT commit)
└── ...
```

---

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hunkue/chinese-idiom-chain-game.git
cd chinese-idiom-chain-game
```

### 2. Install System Dependencies (macOS)

```bash
brew install mysql pkg-config
```

### 3. Set Up Virtual Environment with uv

```bash
uv venv
uv init  # Only needed once if pyproject.toml does not exist
```

### 4. Add Required Python Packages

```bash
uv add aioconsole cryptography mysqlclient pymysql python-dotenv 
```

> (Alternatively, use `PyMySQL` instead of `mysqlclient` if you prefer pure Python drivers)

---

### 5. Setup `.env` File

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

### 6. Create and Initialize MySQL Database

```sql
CREATE DATABASE game_db CHARACTER SET utf8mb4;

USE game_db;

CREATE TABLE idioms (
    id INT AUTO_INCREMENT PRIMARY KEY,
    idiom VARCHAR(20) NOT NULL,
    definition TEXT
);

CREATE TABLE records (
    id INT AUTO_INCREMENT PRIMARY KEY,
    player_name VARCHAR(50),
    score INT,
    timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
);
```

Import idiom data into the `idioms` table.

---

### 7. Run the Application

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
- 🎨 tkinter-based GUI
- 🌐 Future Django web version in progress

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