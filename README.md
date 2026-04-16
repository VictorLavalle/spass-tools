# spass-tools

Encrypt and decrypt Samsung Pass `.spass` files. Convert passwords between `.spass` and CSV formats.

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

The CSV file must have these columns:

| Column | Description |
|--------|-------------|
| `Title` | Name of the site or app |
| `URL` | Website or app URL |
| `Username` | Login username or email |
| `Password` | Password |
| `Notes` | Optional notes |
| `OTPAuth` | Optional OTP auth URI |

---

## `.spass` Format Reference

### Encryption
| Parameter | Value |
|-----------|-------|
| Algorithm | AES-256-CBC |
| Key derivation | PBKDF2-HMAC-SHA256 |
| Iterations | 70,000 |
| Salt | 20 random bytes |
| IV | 16 random bytes |
| Padding | PKCS7 |
| File encoding | `base64(salt + iv + encrypted_data)` |

### Internal Structure
Line separator: `\r\n` (CRLF)

```
30                                    ← format version
true;false;false;false                ← modules (passwords;cards;addresses;notes)
false                                 ← unknown field (new in v25+)
next_table                            ← section delimiter
_id;origin_url;action_url;...         ← header (35 semicolon-separated fields)
<base64>;<base64>;...                 ← data rows (each field base64-encoded)
```

### Password Record Fields (35 total)
| # | Field | Value |
|---|-------|-------|
| 0 | `_id` | Incremental ID |
| 1 | `origin_url` | Site URL |
| 2 | `action_url` | `&&&NULL&&&` |
| 3 | `username_element` | empty |
| 4 | `username_value` | Username |
| 5 | `id_tz_enc` | `&&&NULL&&&` |
| 6 | `password_element` | empty |
| 7 | `password_value` | Password |
| 8 | `pw_tz_enc` | `&&&NULL&&&` |
| 9 | `host_url` | Same as origin_url |
| 10 | `ssl_valid` | `0` |
| 11 | `preferred` | `0` |
| 12 | `blacklisted_by_user` | `0` |
| 13 | `use_additional_auth` | `1` |
| 14 | `cm_api_support` | `&&&NULL&&&` |
| 15 | `created_time` | Timestamp (ms) |
| 16 | `modified_time` | Timestamp (ms) |
| 17 | `title` | Site/app name |
| 18 | `favicon` | PNG bytes or empty |
| 19 | `source_type` | `2` |
| 20 | `app_name` | App name |
| 21 | `package_name` | Android package or empty |
| 22 | `package_signature` | Package signature or empty |
| 23–30 | `reserved_1`–`reserved_8` | `&&&NULL&&&` (except `reserved_2` = `0`) |
| 31 | `credential_memo` | Notes |
| 32 | `otp` | OTP auth URI |
| 33 | `root_id` | `&&&NULL&&&` |
| 34 | `parent_id` | `&&&NULL&&&` |

> **Note**: Null fields use `&&&NULL&&&` (3 ampersands each side). Fields `username_element` and `password_element` are actual empty strings.

---

## Acknowledgments

Huge thanks to [0xdeb7ef](https://github.com/0xdeb7ef) and their [spass-manager](https://github.com/0xdeb7ef/spass-manager) project. Their reverse engineering of the `.spass` format and decryption logic was essential to building these tools. Without their work, this project wouldn't exist.

## License

[MIT](LICENSE)
