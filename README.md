# spass-tools

[![License: MIT](https://img.shields.io/github/license/VictorLavalle/spass-tools)](LICENSE)
[![Python 3.8+](https://img.shields.io/badge/python-3.8%2B-blue)](https://www.python.org/downloads/)
[![Release](https://img.shields.io/github/v/release/VictorLavalle/spass-tools)](https://github.com/VictorLavalle/spass-tools/releases)
[![CI](https://github.com/VictorLavalle/spass-tools/actions/workflows/ci.yml/badge.svg)](https://github.com/VictorLavalle/spass-tools/actions/workflows/ci.yml)

Encrypt and decrypt Samsung Pass `.spass` files. Convert passwords between `.spass` and CSV formats.

## Table of Contents

- [Quick Start](#quick-start)
- [Exporting from Samsung Pass](#exporting-from-samsung-pass)
- [Usage](#usage)
- [Importing into Samsung Pass](#importing-into-samsung-pass)
- [CSV Format](#csv-format)
- [.spass Format Reference](#spass-format-reference)
- [Troubleshooting](#troubleshooting)
- [Contributing](#contributing)
- [Acknowledgments](#acknowledgments)
- [License](#license)

## Quick Start

### Prerequisites
- [Python 3.8+](https://www.python.org/downloads/) (check "Add to PATH" during install on Windows)

### Download
```bash
git clone https://github.com/VictorLavalle/spass-tools.git
cd spass-tools
```

Or download as ZIP from the [releases page](https://github.com/VictorLavalle/spass-tools/releases).

---

## Exporting from Samsung Pass

1. Open the **Samsung Wallet** app on your phone

   <img width="270" alt="image" src="https://github.com/user-attachments/assets/9f10f5d7-2319-4d13-a4ff-e7e311240616" />

2. Tap the **⋮** (three dots) button in the top-right corner

   <img width="270" alt="image" src="https://github.com/user-attachments/assets/40a8eee2-6622-4970-8371-b04c7982e206" />

3. Tap **Settings**

   <img width="270" alt="image" src="https://github.com/user-attachments/assets/b4b67fe1-b0a4-4690-8f3d-12f809ede581" />

4. Tap **Import and export Samsung Pass data**

   <img width="270" alt="image" src="https://github.com/user-attachments/assets/fa82956c-69be-4efc-b920-372b4a72df18" />

5. Select **Export** and set a password — this generates the `.spass` file

   <img width="270" alt="image" src="https://github.com/user-attachments/assets/1b020dae-0a78-4b37-8099-5fbd82a6a7ea" /> <img width="270" alt="image" src="https://github.com/user-attachments/assets/94424b5a-d4cc-4eea-8910-ce958e326461" />

6. Transfer the `.spass` file to your computer

   <img width="400" alt="image" src="https://github.com/user-attachments/assets/04c1a230-6066-41c5-90d2-46a74567fad3" />

---

## Usage
<img width="444" height="331" alt="image" src="https://github.com/user-attachments/assets/bb631ab0-02f9-4b9c-bac1-e71ab894628b" />



### macOS / Linux

Run the unified tool:
```bash
./spass_tools.sh
```

Or run encrypt/decrypt directly:
```bash
./decrypt.sh    # .spass → CSV
./encrypt.sh    # CSV → .spass
```

### Windows

Double-click `spass_tools.bat`

Or run individually: `decrypt.bat` / `encrypt.bat`

### All scripts will:
1. Check that Python is installed
2. Auto-install dependencies if needed
3. Auto-detect files in the current folder
4. Open a file browser if you need to pick a different file
5. Ask for the password securely (hidden input)

### Advanced (command line)

```bash
pip3 install -r requirements.txt

python3 spass_to_csv.py backup.spass passwords.csv "mypassword"
python3 csv_to_spass.py passwords.csv backup.spass "mypassword"
```

If you omit the password argument, it will be prompted interactively.

---

## Importing into Samsung Pass

1. Transfer the generated `.spass` file to your phone
2. Open the **Samsung Wallet** app
3. Tap the **⋮** (three dots) button in the top-right corner
4. Tap **Settings**
5. Tap **Import and export Samsung Pass data**
6. Select **Import** and choose the `.spass` file
7. Enter the password you used during encryption

<!-- TODO: Add screenshots -->

---

## CSV Format

The tool auto-detects columns from the most common password managers:

| Source | Columns |
|--------|---------|
| Apple Passwords (Mac) | `Title,URL,Username,Password,Notes,OTPAuth` |
| Google Passwords | `name,url,username,password,note` |
| Chrome / Brave | `name,url,username,password,note` |
| LastPass | `url,username,password,extra,name,grouping,fav` |
| Bitwarden | `folder,favorite,type,name,notes,fields,reprompt,login_uri,login_username,login_password,login_totp` |
| 1Password | `Title,Url,Username,Password,Notes,Type` |

Any CSV with similar column names will work — the tool matches columns case-insensitively.

---

## `.spass` Format Reference

See [docs/FORMAT.md](docs/FORMAT.md) for the full `.spass` file format specification, including encryption parameters, internal structure, and all 35 password record fields.

---

## Troubleshooting

| Problem | Solution |
|---------|----------|
| `Wrong password or corrupted file` | Double-check the password. It must match exactly what was used during export/encryption. |
| `Python not found` | Install [Python 3.8+](https://www.python.org/downloads/). On Windows, check "Add to PATH" during install. |
| `No module named 'cryptography'` | Run `pip3 install -r requirements.txt` or let the scripts auto-install dependencies. |
| `No .spass/.csv files found` | Place the file in the same folder as the scripts, or use the file browser when prompted. |
| `Password must include at least 3 of...` | Samsung Pass requires 8+ characters with at least 3 of: uppercase, lowercase, numbers, special characters. |

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines on how to contribute, report bugs, and submit pull requests.

For security vulnerabilities, see [SECURITY.md](SECURITY.md).

This project follows a [Code of Conduct](CODE_OF_CONDUCT.md).

---

## Acknowledgments

Huge thanks to [0xdeb7ef](https://github.com/0xdeb7ef) and their [spass-manager](https://github.com/0xdeb7ef/spass-manager) project. Their reverse engineering of the `.spass` format and decryption logic was essential to building these tools. Without their work, this project wouldn't exist.

## License

[MIT](LICENSE)
