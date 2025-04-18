# Chinese Idiom Chain Game

![Python version](https://img.shields.io/badge/python-3.10%2B-blue)
![License](https://img.shields.io/badge/license-MIT-green)
![Repo size](https://img.shields.io/github/repo-size/hunkue/chinese-idiom-chain-game)
![Last commit](https://img.shields.io/github/last-commit/hunkue/chinese-idiom-chain-game)
![Issues](https://img.shields.io/github/issues/hunkue/chinese-idiom-chain-game)


This is a Python-based **Chinese idiom chain game** supporting both Command Line Interface (CLI) and Graphical User Interface (GUI using `tkinter`).  
It integrates with a MySQL database to retrieve idioms and store player records. In the future, the game will be deployed to a personal website via Django: [hunkue.com](https://hunkue.com).

## 📁 Project Structure

```
chinese-idiom-chain-game/
├── idiom_chain.py             # Main GUI program
├── game.py                    # Core game logic
├── game_timer.py              # Countdown timer module
├── records_database.py        # Game record database handler
├── idiom_database.py          # Idiom database loader
├── requirements.txt           # Python dependencies
├── .env                       # Environment variable configuration (DO NOT upload)
└── ...
```

## 🚀 Getting Started

### 1. Clone the Repository

```bash
git clone https://github.com/hunkue/chinese-idiom-chain-game.git
cd chinese-idiom-chain-game
```

### 2. Create a Virtual Environment

```bash
python3 -m venv .venv
source .venv/bin/activate      # macOS / Linux
# .venv\Scripts\activate     # Windows
```

### 3. Install Dependencies

Install packages with:

```bash
pip install -r requirements.txt
```

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

### 5. Create and Initialize MySQL Database

You’ll need to set up a MySQL database named `game_db` and create the required tables:

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

Populate the `idioms` table with your idiom dataset.

### 6. Run the Application

#### Run the GUI version

```bash
python idiom_chain.py
```

#### Run the CLI version (if `main.py` is available)

```bash
python main.py
```

---

## ✨ Features

- 🧠 Automatic idiom prompts and answer validation
- ⏱️ 30-second countdown timer for each turn
- 💾 Persistent storage of idioms and player scores in MySQL
- 🎨 Interactive GUI built with `tkinter`
- 🌐 Future deployment via Django on [hunkue.com](https://hunkue.com)

## 🛠️ Development Environment

- Python 3.10+
- `tkinter`
- `pymysql`
- `.env` for configuration
- MySQL 8.0+

---

## 🤝 Contributing

Issues and pull requests are welcome!  
Feel free to open an issue or reach out if you’d like to collaborate or suggest improvements.

---

## 📝 License

This project is licensed under the MIT License.  
See [LICENSE](./LICENSE) for more details.