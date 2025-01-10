# ethos

cli music player (Coming Soon)

## Repository Structure

```bash
ethos/
├── .editorconfig
├── .gitignore
├── .github/
│   ├── ISSUE_TEMPLATE/
│   └── workflows/
├── docker/
│   ├── dockerfile
│   ├── compose.yaml
│   └── readme.md
├── ethos/
│   ├── __init__.py
│   ├── main.py    # entry point of the application.
│   ├── config.py  # Manages configuration settings.
│   ├── player.py  # Handles the core functionality of the music player.
│   ├── ui/        # Manages the tui interface.
│   ├── utils.py   # Contains utility functions and other helper functions.
│   └── hotkeys.py # Defines hotkeys for controlling the music player.
├── tests/
│   ├── __init__.py
│   ├── test_cli.py
│   ├── test_config.py
│   ├── test_player.py
│   ├── test_ui.py
│   └── test_utils.py
├── LICENSE
├── README.md
├── setup.py      # Contains the setup script
└── requirements.txt
```

## Installation

### For Development:

1. **Clone the Repository:**
   ```bash
   git clone https://github.com//Itz-Agasta/ethos.git
   cd ethos
   ```
2. **Set Up a Virtual Environment:**

   ```bash
   python -m venv .venv
   source .venv/bin/activate       # For MacOS/Linux
   .venv\Scripts\activate          # For Windows
   ```

3. **Install Dependencies:**
   ```python
   pip install -r requirements.txt
   ```
4. **Setup the .env file:** see the `.env.example` for reference and create a `.env` file in the root.

### For Distribution:

Coming Soon
