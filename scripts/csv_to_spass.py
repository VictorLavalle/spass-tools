#!/usr/bin/env python3
"""Convert a CSV password file to Samsung Pass .spass format."""
import csv, os, sys, base64, hashlib, time, getpass
os.environ['TK_SILENCE_DEPRECATION'] = '1'
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives import padding

NULL = '&&&NULL&&&'
ITERATION_COUNT = 70000
KEY_LENGTH = 32
SALT_BYTES = 20
BLOCK_SIZE = 16

def b64e(s):
    """Base64 encode a string."""
    return base64.b64encode(s.encode('utf-8')).decode('utf-8')

def pkcs7_pad(data):
    padder = padding.PKCS7(128).padder()
    return padder.update(data) + padder.finalize()

def encrypt_spass(plaintext, password):
    """Encrypt plaintext using the spass format: base64(salt + iv + aes_cbc(data))"""
    salt = os.urandom(SALT_BYTES)
    iv = os.urandom(BLOCK_SIZE)
    key = hashlib.pbkdf2_hmac('sha256', password.encode('utf-8'), salt, ITERATION_COUNT, dklen=KEY_LENGTH)
    cipher = Cipher(algorithms.AES(key), modes.CBC(iv))
    encryptor = cipher.encryptor()
    padded = pkcs7_pad(plaintext)
    encrypted = encryptor.update(padded) + encryptor.finalize()
    return base64.b64encode(salt + iv + encrypted)

def build_password_row(idx, url, username, password, title, notes, otp):
    """Build a single password row with 35 base64-encoded fields separated by ;"""
    now_ms = str(int(time.time() * 1000))
    fields = [
        str(idx),           # _id
        url,                # origin_url
        NULL,               # action_url
        '',                 # username_element
        username,           # username_value
        NULL,               # id_tz_enc
        '',                 # password_element
        password,           # password_value
        NULL,               # pw_tz_enc
        url,                # host_url
        '0',                # ssl_valid
        '0',                # preferred
        '0',                # blacklisted_by_user
        '1',                # use_additional_auth
        NULL,               # cm_api_support
        now_ms,             # created_time
        now_ms,             # modified_time
        title,              # title
        '',                 # favicon
        '2',                # source_type
        title,              # app_name
        '',                 # package_name
        '',                 # package_signature
        NULL,               # reserved_1
        '0',                # reserved_2
        NULL,               # reserved_3
        NULL,               # reserved_4
        NULL,               # reserved_5
        NULL,               # reserved_6
        NULL,               # reserved_7
        NULL,               # reserved_8
        notes,              # credential_memo
        otp,                # otp
        NULL,               # root_id
        NULL,               # parent_id
    ]
    return ';'.join(b64e(f) for f in fields)

def validate_password(password):
    """Validate password meets Samsung Pass requirements:
    At least 8 characters, including at least 3 of: uppercase, lowercase, numbers, special chars."""
    if len(password) < 8:
        return False, "Password must be at least 8 characters."
    categories = 0
    if any(c.isupper() for c in password): categories += 1
    if any(c.islower() for c in password): categories += 1
    if any(c.isdigit() for c in password): categories += 1
    if any(c in '!@#$%^&*?' for c in password): categories += 1
    if categories < 3:
        return False, "Password must include at least 3 of: uppercase, lowercase, numbers, special characters (!@#$%^&*?)."
    return True, ""

def csv_to_spass(csv_path, spass_path, password):
    """Read a CSV file and encrypt it into .spass format."""
    with open(csv_path, newline='', encoding='utf-8-sig') as f:
        rows = list(csv.DictReader(f))

    if not rows:
        print("\n  No rows found in CSV.")
        sys.exit(1)

    # Auto-detect column names (support multiple CSV formats)
    # Supported: Apple Passwords, Google/Chrome/Brave, LastPass, Bitwarden, 1Password
    cols = list(rows[0].keys())
    col_map = {}
    for key in cols:
        k = key.strip().lower()
        if k in ('title', 'name'):                          col_map['title'] = key
        elif k in ('url', 'login_uri'):                     col_map['url'] = key
        elif k in ('username', 'user', 'login_username'):   col_map['username'] = key
        elif k in ('password', 'pass', 'login_password'):   col_map['password'] = key
        elif k in ('notes', 'note', 'extra'):               col_map['notes'] = key
        elif k in ('otpauth', 'otp', 'login_totp'):         col_map['otp'] = key

    if 'password' not in col_map:
        print(f"\n  Could not find a password column in: {cols}")
        sys.exit(1)

    header = '_id;origin_url;action_url;username_element;username_value;id_tz_enc;password_element;password_value;pw_tz_enc;host_url;ssl_valid;preferred;blacklisted_by_user;use_additional_auth;cm_api_support;created_time;modified_time;title;favicon;source_type;app_name;package_name;package_signature;reserved_1;reserved_2;reserved_3;reserved_4;reserved_5;reserved_6;reserved_7;reserved_8;credential_memo;otp;root_id;parent_id'

    lines = ['30', 'true;false;false;false', 'false', 'next_table', header]
    count = 0
    for i, r in enumerate(rows, 1):
        url = r.get(col_map.get('url', ''), '').strip()
        username = r.get(col_map.get('username', ''), '').strip()
        pwd = r.get(col_map.get('password', ''), '').strip()
        title = r.get(col_map.get('title', ''), '').strip()
        notes = r.get(col_map.get('notes', ''), '').strip()
        otp = r.get(col_map.get('otp', ''), '').strip()
        if not pwd:
            continue
        if not notes:
            notes = NULL
        if not otp:
            otp = NULL
        lines.append(build_password_row(i, url, username, pwd, title, notes, otp))
        count += 1

    plaintext = '\r\n'.join(lines).encode('utf-8')
    encrypted = encrypt_spass(plaintext, password)

    with open(spass_path, 'wb') as f:
        f.write(encrypted)

    print(f"\n  Done! {count} passwords encrypted.")
    print(f"  Output: {spass_path}\n")

def open_file_dialog(title, filetypes):
    """Open a native file picker dialog. Returns path or empty string."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.askopenfilename(title=title, filetypes=filetypes)
        root.destroy()
        return path
    except:
        return ''

def save_file_dialog(title, filetypes, defaultext, initialfile=''):
    """Open a native save file dialog. Returns path or empty string."""
    try:
        import tkinter as tk
        from tkinter import filedialog
        root = tk.Tk()
        root.withdraw()
        root.attributes('-topmost', True)
        path = filedialog.asksaveasfilename(title=title, filetypes=filetypes, defaultextension=defaultext, initialfile=initialfile)
        root.destroy()
        return path
    except:
        return ''

def find_csv_files():
    """Find .csv files in the script's directory."""
    script_dir = os.path.dirname(os.path.dirname(os.path.abspath(__file__)))
    return sorted(f for f in os.listdir(script_dir) if f.endswith('.csv'))

def main():
    print("")
    print("  ╔══════════════════════════════════════════════╗")
    print("  ║   CSV → Samsung Pass (.spass) Converter   ║")
    print("  ╚══════════════════════════════════════════════╝")
    print("")

    if len(sys.argv) >= 3:
        csv_path, spass_path = sys.argv[1], sys.argv[2]
    else:
        csv_files = find_csv_files()
        if len(csv_files) == 1:
            csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), csv_files[0])
            print(f"  Found: {csv_files[0]}")
            use = input("  Use this file? (Y/n): ").strip().lower()
            if use and use != 'y':
                csv_path = open_file_dialog("Select CSV file", [("CSV", "*.csv"), ("All files", "*.*")])
                if not csv_path:
                    csv_path = input("\n  CSV file path: ").strip().strip("'\"")
        elif len(csv_files) > 1:
            print("  Found multiple CSV files:\n")
            for i, f in enumerate(csv_files, 1):
                print(f"     {i}. {f}")
            print(f"     {len(csv_files)+1}. Browse for a different file...")
            choice = input(f"\n  Select (1-{len(csv_files)+1}): ").strip()
            idx = int(choice) if choice.isdigit() else 0
            if idx == len(csv_files) + 1:
                csv_path = open_file_dialog("Select CSV file", [("CSV", "*.csv"), ("All files", "*.*")])
                if not csv_path:
                    csv_path = input("\n  CSV file path: ").strip().strip("'\"")
            elif 1 <= idx <= len(csv_files):
                csv_path = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), csv_files[idx - 1])
            else:
                print("\n  Invalid selection.")
                sys.exit(1)
        else:
            print("  No CSV files found in this folder.")
            csv_path = open_file_dialog("Select CSV file", [("CSV", "*.csv"), ("All files", "*.*")])
            if not csv_path:
                csv_path = input("  CSV file path: ").strip().strip("'\"")
            else:
                print(f"  Selected: {csv_path}")

        default_spass = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), 'output.spass')
        print(f"\n  Default output: {default_spass}")
        print(f"    1. Save here (press Enter)")
        print(f"    2. Choose a different location")
        choice = input("  Select [1]: ").strip()
        if choice == '2':
            spass_path = save_file_dialog("Save .spass file", [("Samsung Pass", "*.spass")], ".spass", "output.spass")
            if not spass_path:
                spass_path = input("  Output .spass path: ").strip().strip("'\"")
            else:
                print(f"  Selected: {spass_path}")
        else:
            spass_path = default_spass

    if not os.path.isfile(csv_path):
        print(f"\n  File not found: {csv_path}")
        sys.exit(1)

    if len(sys.argv) >= 4:
        password = sys.argv[3]
    else:
        print("")
        print("  Password requirements (Samsung Pass):")
        print("    - At least 8 characters")
        print("    - At least 3 of: uppercase, lowercase, numbers, special (!@#$%^&*?)")
        print("")
        password = getpass.getpass("  Encryption password: ")
        confirm = getpass.getpass("  Confirm password: ")
        if password != confirm:
            print("\n  Passwords don't match.")
            sys.exit(1)

    if not password:
        print("\n  Password cannot be empty.")
        sys.exit(1)

    valid, msg = validate_password(password)
    if not valid:
        print(f"\n  {msg}")
        sys.exit(1)

    print("\n  Encrypting...")
    csv_to_spass(csv_path, spass_path, password)

if __name__ == '__main__':
    main()
